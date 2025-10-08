from typing import List, Dict, Any, Optional


def paginate_data(
    datas: List[Dict[str, Any]],
    page: int = 1,
    size: int = 10,
    sort_key: Optional[str] = None,
    reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    对包含字典的列表进行分页处理，并支持排序功能
    
    Args:
        datas: 要分页的数据源列表
        page: 要获取的页码（从1开始）
        size: 每页的数据条数
        sort_key: 排序的键名，如果为None则不排序
        reverse: 是否倒序排列
    
    Returns:
        分页后的结果列表
    
    Raises:
        ValueError: 当传入的参数无效时抛出异常
    """
    # 参数验证
    if page < 1:
        raise ValueError("页码必须大于等于1")
    if size < 1:
        raise ValueError("每页条数必须大于等于1")
    if sort_key is not None:
        # 检查所有字典是否都包含sort_key
        if not all(sort_key in item for item in datas):
            raise ValueError(f"所有字典必须包含排序键 '{sort_key}'")
    
    # 排序数据
    sorted_data = sorted(datas, key=lambda x: x[sort_key], reverse=reverse) if sort_key is not None else datas
    
    # 计算分页的起始和结束索引
    start_index = (page - 1) * size
    end_index = start_index + size
    
    # 返回分页后的结果
    return sorted_data[start_index:end_index]
