# aqiyi_bullet_crawler
爱奇艺弹幕爬虫

## 流程概述

- 获取《XXXX》所有已发布剧集的视频编号（tv_id）：
get_tv_id(aid)函数，手动输入该剧的AID,获取分集的tv_id

- 请求弹幕 API
https://cmts.iqiyi.com/bullet/tv_id[-4:-2]/tv_id[-2:]/tv_id_300_x.z
https://cmts.iqiyi.com/bullet/视频编号的倒数4、3位/视频编号的倒数2、1位/视频编号_300_序号.z
弹幕文件每5分钟（300秒）向服务器请求一次，故每集弹幕文件数量等于视频时间(秒)除以300之后向上取整，实际编程时这里可以简单处理

- 返回数据
格式为压缩包gzip，解压后为xml

- 数据解析
XML解析方式

- 保存至本地CSV
