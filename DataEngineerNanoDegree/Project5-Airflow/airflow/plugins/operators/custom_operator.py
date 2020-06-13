from airflow.models import BaseOperator

class MyClass(BaseOperator):
    def __init__(self, arg1, arg2, **kwargs):
        self.arg1 = arg1
        self.arg2 = arg2

    def execute(self):
        myvar = self.arg1
