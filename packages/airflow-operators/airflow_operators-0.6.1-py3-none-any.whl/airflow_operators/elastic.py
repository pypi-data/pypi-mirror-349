from typing import Any, Callable

from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonOperator
from elasticsearch import Elasticsearch


class ElasticsearchCustomHook(BaseHook):
    conn_name_attr = "elasticsearch_conn_id"
    default_conn_name = "elasticsearch_default"
    conn_type = "elasticsearch_custom"
    hook_name = "ElasticsearchCustom"

    def __init__(self, conn_id: str):
        super().__init__()
        self.conn_id = conn_id

    def get_conn(self) -> Any:
        conn = self.get_connection(self.conn_id)
        hosts = [f'https://{conn.host}:{conn.port}']
        api_key = conn.get_password()

        client = Elasticsearch(hosts=hosts, api_key=api_key, **conn.extra_dejson)
        return client


class ElasticsearchBulkOperator(PythonOperator):
    """Выполняет bulk, формируемый в python_callable"""

    def __init__(
        self,
        conn_id: str,
        index_name: str,
        python_callable: Callable,
        *args,
        **kwargs,
    ):
        super().__init__(*args, python_callable=python_callable, **kwargs)
        self.conn_id = conn_id
        self.index_name = index_name

    def execute_callable(self):
        hook = ElasticsearchCustomHook(self.conn_id)

        with hook.get_conn() as conn:
            bulk = self.python_callable(
                *self.op_args,
                **self.op_kwargs,
            )

            if bulk:
                result = conn.bulk(index=self.index_name, body=bulk)
                self.check_errors(result)

    @staticmethod
    def check_errors(result):
        if result["errors"]:
            errors = []

            for item in result["items"]:
                operation = next(iter(item))

                error_info = item[operation].get("error")

                if error_info and error_info.get("type") != "document_missing_exception":
                    errors.append(
                        {"operation": operation, "id": item[operation]["_id"], "error": error_info}
                    )
            if errors:
                raise ValueError(f"Bulk operation failed with errors: {errors}")
