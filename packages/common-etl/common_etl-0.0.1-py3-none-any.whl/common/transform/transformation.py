from abc import ABC, abstractmethod


class AbstractLogicFunction(ABC):

    @abstractmethod
    def execute(self, target_data_frame, source_data_frame, target_column_name):
        pass


class ColumnConfig:
    def __init__(self, target_column: str, logic_function: AbstractLogicFunction):
        self.target_column = target_column
        self.logic_function = logic_function


class CopyFromSource(AbstractLogicFunction):
    def __init__(self, source_column_name: str):
        self.source_column_name = source_column_name

    def execute(self, target_data_frame, source_data_frame, target_column_name):
        target_data_frame[target_column_name] = source_data_frame[
            self.source_column_name
        ].astype(str)
        return target_data_frame


class CopyFromConstant(AbstractLogicFunction):
    def __init__(self, constant: str):
        self.constant = constant

    def execute(self, target_data_frame, source_data_frame, target_column_name):
        target_data_frame[target_column_name] = self.constant
        return target_data_frame
