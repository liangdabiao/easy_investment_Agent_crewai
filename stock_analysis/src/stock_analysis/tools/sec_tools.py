import os
from typing import Any, Optional, Type
from pydantic.v1 import BaseModel, Field
from crewai_tools import RagTool
from sec_api import QueryApi  # Make sure to have sec_api installed
import requests
import html2text
import re

# 为了兼容 Pydantic v2 API，添加一个兼容层
class CompatibilityBaseModel(BaseModel):
    @classmethod
    def get_model_fields(cls):
        return cls.__fields__
    
    # 自定义一个兼容层，确保ModelField对象有description属性
    class ModelFieldCompat:
        def __init__(self, field_info):
            self.field_info = field_info
            # 确保description属性存在
            self.description = getattr(field_info, 'description', '')
            # 复制其他可能需要的属性
            for attr in dir(field_info):
                if not attr.startswith('__') and not hasattr(self, attr):
                    setattr(self, attr, getattr(field_info, attr))
    
    # 为类添加 model_fields 属性，将每个字段包装在兼容层中
    @classmethod
    @property
    def model_fields(cls):
        result = {}
        for name, field_info in cls.__fields__.items():
            result[name] = cls.ModelFieldCompat(field_info)
        return result

class FixedSEC10KToolSchema(CompatibilityBaseModel):
    """Input for SEC10KTool."""
    search_query: str = Field(
        ...,
        description="Mandatory query you would like to search from the 10-K report",
    )

class SEC10KToolSchema(CompatibilityBaseModel):
    """Input for SEC10KTool."""
    stock_name: str = Field(
        ..., description="Mandatory valid stock name you would like to search"
    )
    search_query: str = Field(
        ..., description="Mandatory query you would like to search from the 10-K report"
    )

class SEC10KTool(RagTool):
    name: str = "Search in the specified 10-K form"
    description: str = "A tool that can be used to semantic search a query from a 10-K form for a specified company."
    args_schema: Type[BaseModel] = SEC10KToolSchema

    def __init__(self, stock_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if stock_name is not None:
            content = self.get_10k_url_content(stock_name)
            if content:
                self.add(content)
                self.description = f"A tool that can be used to semantic search a query from {stock_name}'s latest 10-K SEC form's content as a txt file."
                self.args_schema = FixedSEC10KToolSchema
                # 避免调用 _generate_description()

    def get_10k_url_content(self, stock_name: str) -> Optional[str]:
        """Fetches the URL content as txt of the latest 10-K form for the given stock name."""
        try:
            queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{stock_name} AND formType:\"10-K\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }
            filings = queryApi.get_filings(query)['filings']
            if len(filings) == 0:
                print("No filings found for this stock.")
                return None

            url = filings[0]['linkToFilingDetails']
            
            headers = {
                "User-Agent": "crewai.com bisan@crewai.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode("utf-8"))

            text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
            return text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error fetching 10-K URL: {e}")
            return None

    def add(self, *args: Any, **kwargs: Any) -> None:
        # Don't set data_type since the current version of crewai_tools doesn't expect it this way
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> Any:
        return super()._run(query=search_query, **kwargs)


class FixedSEC10QToolSchema(CompatibilityBaseModel):
    """Input for SEC10QTool."""
    search_query: str = Field(
        ...,
        description="Mandatory query you would like to search from the 10-Q report",
    )

class SEC10QToolSchema(CompatibilityBaseModel):
    """Input for SEC10QTool."""
    stock_name: str = Field(
         description="Mandatory valid stock name you would like to search"
    )
    search_query: str = Field(
        ..., description="Mandatory query you would like to search from the 10-Q report"
    )

class SEC10QTool(RagTool):
    name: str = "Search in the specified 10-Q form"
    description: str = "A tool that can be used to semantic search a query from a 10-Q form for a specified company."
    args_schema: Type[BaseModel] = SEC10QToolSchema

    def __init__(self, stock_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if stock_name is not None:
            content = self.get_10q_url_content(stock_name)
            if content:
                self.add(content)
                self.description = f"A tool that can be used to semantic search a query from {stock_name}'s latest 10-Q SEC form's content as a txt file."
                self.args_schema = FixedSEC10QToolSchema
                # 避免调用 _generate_description()

    def get_10q_url_content(self, stock_name: str) -> Optional[str]:
        """Fetches the URL content as txt of the latest 10-Q form for the given stock name."""
        try:
            queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{stock_name} AND formType:\"10-Q\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }
            filings = queryApi.get_filings(query)['filings']
            if len(filings) == 0:
                print("No filings found for this stock.")
                return None

            url = filings[0]['linkToFilingDetails']
            
            headers = {
                "User-Agent": "crewai.com bisan@crewai.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode("utf-8"))

            # Removing all non-English words, dollar signs, numbers, and newlines from text
            text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
            return text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error fetching 10-Q URL: {e}")
            return None

    def add(self, *args: Any, **kwargs: Any) -> None:
        # Don't set data_type since the current version of crewai_tools doesn't expect it this way
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> Any:
        return super()._run(query=search_query, **kwargs)

