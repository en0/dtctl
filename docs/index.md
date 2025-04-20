# DotFiles Control

This is a WIP to orginize my thoughts during dev.
Eventually this will be used to store documentation about the tool.

## Concepts

Dotfiles are managed through a collection of files called a host configuration collection, HCC. An
HCC is a collection of configuration sets which is a set of individual configuration files.

For example, An HCC might include configurations for Polybar and i3. The Polybar configuration set
might include two files and the i3 configuration set might include one file.

![Simple HCC Example](assets/img/diagrams/SimpleHCC.png)

## Future Considerations

### Transaction Management Strategy for `ConfigSetService`

1. **Objective**: 
   - Ensure atomic operations within the `ConfigSetService`, particularly for methods like `add_files`, to maintain consistency and prevent partial updates.

2. **Approach Considered**:
   - **Unit of Work (UoW) Pattern**: Initially considered for managing transactions across multiple components (e.g., file handlers and repositories) to ensure all operations are committed or rolled back together.
   - **Compensating Transaction Pattern**: Leaning towards this approach due to its simplicity and adequacy for the current needs. It involves defining compensating actions to undo partial changes if an error occurs, without the complexity of full transaction management.

3. **Rationale for Compensating Transactions**:
   - **Simplicity**: Easier to implement compared to a full transaction management system.
   - **Low Risk**: The likelihood of a user causing significant issues is low, making this approach sufficient for maintaining consistency.
   - **Error Handling**: Focuses on handling errors gracefully by rolling back changes through predefined compensating actions.

4. **Implementation Considerations**:
   - **Context Manager**: Use a `CompensatingTransaction` context manager within service methods to manage the lifecycle of operations, ensuring atomicity and consistency.
   - **Error Management**: Leverage existing error classes (e.g., `OperationFailedError`) to handle and report errors effectively during transaction operations.

**Compensating Transaction Example**

```python
class CompensatingTransaction:

    def __init__(self):
        self._compensations = []

    def register_compensation(self, delegate):
        self._compensations.append(delegate)

    def rollback(self):
        for compensation in reverse(self._compensations):
            try:
                compensation()
            except:
                log.exception("Failed to rollback transaction.")

    @staticmethod
    @contextmanager
    def start_transaction():
        t = CompensatingTransaction()
        try:
            yield t

        except:
            t.rollback()


def main():

    repo = Repository()
    handler = FileHandler()

    config_set = repo.find_by_id("MyConfig")
    original_config_set = config_set.clone()

    with CompensatingTransaction.start_transaction() as trx:
        for file_name, data in {"foo": b"hello", "bar": b"world"}.items():

            entity = ConfigSetEntity(uuid4(), file_name)

            # Register a compensation incase the something failes before we exit the context.
            handler.store(entity.identity, data)
            trx.register_compensation(lambda:handler.remove(entity.identity))

            config_set.files.append(entity)

        # no need to compensate the last thing here.
        # If this completes, we are done.
        repo.update(config_set)
```
