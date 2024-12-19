from enum import Enum
from typing import Optional, Any, List

from pydantic import BaseModel, Field

class MarketSelfInfoRequest(BaseModel):
    """
    GET
    https://secondhand-market.nwpu.edu.cn/api/user/noAvatar
    """
    pass

class MarketSelfInfoData(BaseModel):
    id: str
    account_name: str = Field(alias='accountName')
    user_name: str = Field(alias='userName')
    organization_name: str = Field(alias='organizationName')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class MarketSelfInfoResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: Optional[MarketSelfInfoData] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class MarketItemClassificationRequest(BaseModel):
    """
    GET
    https://secondhand-market.nwpu.edu.cn/api/dict/tree/item-classificationy
    """
    pass


class MarketItemClassificationTypeItem(BaseModel):
    id: str
    parent_id: str = Field(alias='parentId')
    top_id: str = Field(alias='topId')
    code: str
    name: str
    eng_name: str = Field(alias='engName')
    sort: int
    remark: str
    is_deleted: int = Field(alias='isDeleted')
    parent_code: Optional[str] | Any = Field(alias='parentCode', default=None)
    parent_name: Optional[str] | Any = Field(alias='parentName', default=None)
    parent_eng_name: Optional[str] | Any = Field(alias='parentEngName', default=None)


class MarketItemClassificationData(BaseModel):
    id: str
    parent_id: str = Field(alias='parentId')
    top_id: str = Field(alias='topId')
    code: str
    name: str
    eng_name: str = Field(alias='engName')
    sort: int
    remark: str
    is_deleted: int = Field(alias='isDeleted')
    parent_code: Optional[str] | Any = Field(alias='parentCode', default=None)
    parent_name: Optional[str] | Any = Field(alias='parentName', default=None)
    parent_eng_name: Optional[str] | Any = Field(alias='parentEngName', default=None)

    # this is where all real data is
    children: Optional[List[MarketItemClassificationTypeItem | Any]] | Any = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketItemClassificationResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: List[MarketItemClassificationData | Any] | Any = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketComplaintTypeRequest(BaseModel):
    """
    GET
    https://secondhand-market.nwpu.edu.cn/api/dict/tree/complain-status
    """
    pass


class MarketComplaintTypeItem(BaseModel):
    id: str
    parent_id: str = Field(alias='parentId')
    top_id: str = Field(alias='topId')
    code: str
    name: str
    eng_name: str = Field(alias='engName')
    sort: int
    remark: str
    is_deleted: int = Field(alias='isDeleted')
    parent_code: Optional[str] | Any = Field(alias='parentCode', default=None)
    parent_name: Optional[str] | Any = Field(alias='parentName', default=None)
    parent_eng_name: Optional[str] | Any = Field(alias='parentEngName', default=None)


class MarketComplaintTypeData(BaseModel):
    id: str
    parent_id: str = Field(alias='parentId')
    top_id: str = Field(alias='topId')
    code: str
    name: str
    eng_name: str = Field(alias='engName')
    sort: int
    remark: str
    is_deleted: int = Field(alias='isDeleted')
    parent_code: Optional[str] | Any = Field(alias='parentCode', default=None)
    parent_name: Optional[str] | Any = Field(alias='parentName', default=None)
    parent_eng_name: Optional[str] | Any = Field(alias='parentEngName', default=None)

    # this is where all real data is
    children: Optional[List[MarketItemClassificationTypeItem | Any]] | Any = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketComplaintTypeResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: List[MarketItemClassificationData | Any] | Any = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

class MarketCampusInfoRequest(BaseModel):
    """
    GET
    https://secondhand-market.nwpu.edu.cn/api/dict/children/campus
    """
    pass

class MarketCampusInfoItem(BaseModel):
    id: str
    parent_id: str = Field(alias='parentId')
    top_id: str = Field(alias='topId')
    code: str
    name: str
    eng_name: str = Field(alias='engName')
    sort: int
    remark: str
    is_deleted: int = Field(alias='isDeleted')
    parent_code: Optional[str | Any] | Any = Field(alias='parentCode')
    parent_name: Optional[str | Any] | Any = Field(alias='parentName')
    parent_eng_name: Optional[str | Any] | Any = Field(alias='parentEngName')

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketCampusInfoResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: List[MarketCampusInfoItem] | Any = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

class MarketUnreadMessageCountRequest(BaseModel):
    """
    GET
    https://secondhand-market.nwpu.edu.cn/api/message/unReadCount
    """
    pass

class MarketUnreadMessageCountResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: Optional[int] | Any = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

class MarketUserMessageRequest(BaseModel):
    """
    GET
    https://secondhand-market.nwpu.edu.cn/api/message/myMessage
    url params
    """
    current_page: int = Field(alias='current', default=1)
    page_size: int = Field(alias='size', default=10)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        
class MarketUserMessageData(BaseModel):
    records: List
    total: int
    size: int
    current: int
    orders: List[Any] # todo: I have no message to check the structure of this part
    optimize_count_sql: bool = Field(alias='optimizeCountSql')
    hit_count: bool = Field(alias='hitCount')
    search_count: bool = Field(alias='searchCount')
    pages: int
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketUserMessageResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: Optional[MarketUserMessageData] | Any = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
    

class MarketItemOrderByType(str, Enum):
    default = 'default-desc'
    publish_time_descending = 'publish_time-desc'
    price_ascending = 'publish_price-asc'
    price_descending = 'publish_price-desc'

class MarketItemVendingStatus(int, Enum):
    on_sale = 1
    all = 2 # uncertain
    sold = 3

class MarketItemQuestType(int, Enum):
    buy = 0
    sell = 1
    all = 2

class MarketItemListRequest(BaseModel):
    """
    GET
    https://secondhand-market.nwpu.edu.cn/api/second/page
    url params
    """

    # in which order should the items be ordered
    order_by: MarketItemOrderByType = Field(alias='orderBy', default=MarketItemOrderByType.default)

    # unknown
    self: int = Field(default=1)

    # campus name: MarketCampusInfoItem.eng_name (IMPORTANT!!)
    # optional
    campus: Optional[str] | Any = Field(default=None)

    # the status of the item
    # whether the item has been sold or not
    vending_status: MarketItemVendingStatus = Field(alias='status', default=MarketItemVendingStatus.on_sale)

    # query keywords, used for searching service
    keyword: Optional[str] | Any = Field(default=None)

    # page number
    current_page: int = Field(alias='current', default=1)
    page_size: int = Field(alias='size', default=10)

    # type of the request: whether it is a buy or sell request
    quest_type: MarketItemQuestType = Field(alias='releaseType', default=MarketItemQuestType.all)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

    def model_dump(self, **kwargs):
        if not 'by_alias' in kwargs.keys():
            kwargs['by_alias'] = True
        if not 'exclude_none' in kwargs.keys():
            kwargs['exclude_none'] = True

        dumped = super().model_dump(**kwargs)

        dumped['orderBy'] = self.order_by.value
        dumped['status'] = self.vending_status.value
        dumped['releaseType'] = self.quest_type.value

        return dumped

class MarketItemListRecord(BaseModel):
    id: str
    publisher_id: str = Field(alias='publisherId')
    publisher_name: str = Field(alias='publisherName')
    category_id: str = Field(alias='categoryId')
    category_id_label: str = Field(alias='categoryIdLabel')
    image_urls: List[str] | Any = Field(alias='imageUrls')
    thumbnail_link: List[str] | Any = Field(alias='thumbnailLink')
    description: str
    mobile: str
    origin_price: str = Field(alias='originPrice')
    publish_price: str = Field(alias='publishPrice')
    status: int
    view_count: Optional[int] = Field(alias='viewCount', default=0)
    del_status: Any = Field(alias='delStatus')
    create_time: int = Field(alias='createTime')
    transaction_time: Any = Field(alias='transactionTime')
    publish_time: int = Field(alias='publishTime')
    campus: str
    campus_label: str = Field(alias='campusLabel')
    release_type: int = Field(alias='releaseType')
    shelves_way: int = Field(alias='shelvesWay')
    shelves_cause: str = Field(alias='shelvesCause')
    shelves_time: Any = Field(alias='shelvesTime')
    identity_type_code: Any = Field(alias='identityTypeCode')
    identity_type_name: Any = Field(alias='identityTypeName')
    organization_code: Any = Field(alias='organizationCode')
    organization_name: Any = Field(alias='organizationName')
    contact: str
    title: str
    negotiable: bool
    polish_time: Any = Field(alias='polishTime')
    is_default_pic: Any = Field(alias='isDefaultPic')
    terminal_type: Any = Field(alias='terminalType')
    user_account: Any = Field(alias='userAccount')
    collected: int
    reason: str
    audit_list: Any = Field(alias='auditList')
    next_topic_id: Any = Field(alias='nextTopicId')
    self_: bool = Field(alias='self')

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketItemListData(BaseModel):
    records: List[MarketItemListRecord] | Any = Field(default=None)
    total: int
    size: int
    current: int
    orders: List
    optimize_count_sql: bool = Field(alias='optimizeCountSql')
    hit_count: bool = Field(alias='hitCount')
    search_count: bool = Field(alias='searchCount')
    pages: int

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketItemListResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: Optional[MarketItemListData] | Any = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketItemDetailRequest(BaseModel):
    """
    GET
    https://secondhand-market.nwpu.edu.cn/api/second/detail/<item id>
    item id: MarketItemListRecord.id
    """
    pass

class MarketItemDetailUserAccount(BaseModel):
    id: str
    account_id: str = Field(alias='accountId')
    account_name: str = Field(alias='accountName')
    identity_type_id: str = Field(alias='identityTypeId')
    identity_type_code: str = Field(alias='identityTypeCode')
    identity_type_name: str = Field(alias='identityTypeName')
    organization_id: str = Field(alias='organizationId')
    organization_code: str = Field(alias='organizationCode')
    organization_name: str = Field(alias='organizationName')
    user_id: str = Field(alias='userId')
    uid: str
    user_no: str = Field(alias='userNo')
    name: str
    full_name_spelling: str = Field(alias='fullNameSpelling')
    name_spelling: str = Field(alias='nameSpelling')
    email: Any
    phone_number: Any = Field(alias='phoneNumber')
    image_url: Any = Field(alias='imageUrl')
    portrait_url: str = Field(alias='portraitUrl')
    certificate_type_id: Any = Field(alias='certificateTypeId')
    certificate_type_code: Any = Field(alias='certificateTypeCode')
    certificate_type_name: Any = Field(alias='certificateTypeName')
    certificate_number: Any = Field(alias='certificateNumber')
    gender_id: str = Field(alias='genderId')
    gender_code: str = Field(alias='genderCode')
    gender_name: str = Field(alias='genderName')
    nation_id: str = Field(alias='nationId')
    nation_code: str = Field(alias='nationCode')
    nation_name: str = Field(alias='nationName')
    country_id: Any = Field(alias='countryId')
    country_code: Any = Field(alias='countryCode')
    country_name: Any = Field(alias='countryName')
    address_id: Any = Field(alias='addressId')
    address_code: Any = Field(alias='addressCode')
    address_name: Any = Field(alias='addressName')
    base64_avatar: Any = Field(alias='base64Avatar')
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketItemDetailAuditListItem(BaseModel):
    id: str
    topic_id: str = Field(alias='topicId')
    publisher_id: str = Field(alias='publisherId')
    publisher_name: str = Field(alias='publisherName')
    category_id: str = Field(alias='categoryId')
    category_id_label: str = Field(alias='categoryIdLabel')
    image_urls: List[str] = Field(alias='imageUrls')
    thumbnail_link: List[str] = Field(alias='thumbnailLink')
    description: str
    mobile: str
    origin_price: str = Field(alias='originPrice')
    publish_price: str = Field(alias='publishPrice')
    user_id: str = Field(alias='userId')
    status: int
    reason: str
    create_time: int = Field(alias='createTime')
    campus: str
    contact: str
    title: str
    negotiable: bool
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketItemDetailData(BaseModel):
    id: str
    publisher_id: str = Field(alias='publisherId')
    publisher_name: str = Field(alias='publisherName')
    category_id: str = Field(alias='categoryId')
    category_id_label: str = Field(alias='categoryIdLabel')
    image_urls: List[str] = Field(alias='imageUrls')
    thumbnail_link: List[str] = Field(alias='thumbnailLink')
    description: str
    mobile: str
    origin_price: str = Field(alias='originPrice')
    publish_price: str = Field(alias='publishPrice')
    status: int
    view_count: Optional[int] = Field(alias='viewCount', default=0)
    del_status: int = Field(alias='delStatus')
    create_time: int = Field(alias='createTime')
    transaction_time: Any = Field(alias='transactionTime')
    publish_time: int = Field(alias='publishTime')
    campus: str
    campus_label: str = Field(alias='campusLabel')
    release_type: int = Field(alias='releaseType')
    shelves_way: int = Field(alias='shelvesWay')
    shelves_cause: str = Field(alias='shelvesCause')
    shelves_time: Any = Field(alias='shelvesTime')
    identity_type_code: str = Field(alias='identityTypeCode')
    identity_type_name: str = Field(alias='identityTypeName')
    organization_code: str = Field(alias='organizationCode')
    organization_name: str = Field(alias='organizationName')
    contact: str
    title: str
    negotiable: bool
    polish_time: Any = Field(alias='polishTime')
    is_default_pic: bool = Field(alias='isDefaultPic')
    terminal_type: str = Field(alias='terminalType')
    user_account: Optional[MarketItemDetailUserAccount] | Any = Field(alias='userAccount', default=None)
    collected: int
    reason: Any
    audit_list: Optional[List[MarketItemDetailAuditListItem | Any]] | Any = Field(alias='auditList', default=None)
    next_topic_id: str = Field(alias='nextTopicId')
    self_: bool = Field(alias='self')
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class MarketItemDetailResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: Optional[MarketItemDetailData] | Any = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
