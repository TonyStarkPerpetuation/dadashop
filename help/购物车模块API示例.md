# 购物车模块-接口说明

### 流程说明：

用户登陆后，添加购物车通过POST方式将数据添加到redis中，访问购物车页面通过GET方式，发送请求，将redis中所有数据响应给前端页面显示，删除购物车中商品，通过DELETE方式发送请求，删除商品。

购物车页面商品数量增加减少都通过PUT方式，发送state,判断事件状态

购物车页面商品勾选，取消勾选都通过PUT方式，发送state,判断事件状态

购物车页面全选，取消全选通过PUT方式，发送state,判断事件状态

### 一，添加到购物车

**URL：**`127.0.0.1:8000/v1/carts/<username>`

**请求方式**：POST

**请求参数**：JSON

|  参数  | 类型 | 是否必须 |    说明    |
| :----: | :--: | :------: | :--------: |
| sku_id | int  |    是    | 商品sku_id |
| count  | int  |    是    |    数量    |

```python
#请求示例
{
	"sku_id":1001,
	"count":"1",
	}
```

**返回值：**JSON

**响应格式**：

```python
#响应示例：
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                        |
| ----- | -------- | ---- | --------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码 |
| data  | 具体数据 | dict | 与error二选一               |
| error | 错误信息 | char | 与data二选一                |

**skus_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
|  sku_sale_atr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```



**状态码参考**：

| 状态码 | 响应信息         | 原因短语                    |
| ------ | ---------------- | --------------------------- |
| 200    | 正常             | OK                          |
| 30101  | 未找到商品       | SKU query error             |
| 30102  | 传参不正确       | Incorrect pass of reference |
| 30103  | 购买数量超过库存 | exceeds the inventory       |
| 30104  | 未找到用户       | User query error            |



### 二，查询购物车

**URL：**`127.0.0.1:8000/v1/carts/<username>`

**请求方式:** GET

**请求参数：**无

**返回值：**JSON

**响应格式**：

```python
#响应示例：
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                        |
| ----- | -------- | ---- | --------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码 |
| data  | 具体数据 | dict | 与error二选一               |
| error | 错误信息 | char | 与data二选一                |

**sku_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
| sku_sale_attr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```

**状态码参考**

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30104  | 未找到用户 | User query error |



### 三，删除购物车数据

**URL：**`127.0.0.1:8000/v1/carts/<username>`

**请求方式：**DELETE

**请求参数：**

```python
#请求参数示例：
{"sku_id":1001}
```

|  参数  | 类型 | 是否必须 |    说明    |
| :----: | :--: | :------: | :--------: |
| sku_id | int  |    是    | 商品sku_id |

**返回值**：JSON

**响应格式：**

```python
#响应示例
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                            |
| ----- | -------- | ---- | ------------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码参考 |
| data  | 具体数据 | dict | 与error二选一                   |
| error | 错误信息 | char | 与data二选一                    |

**skus_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
|  sku_sale_atr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```



**状态码参考**

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30101  | 未找到商品 | SKU query error  |
| 30104  | 未找到用户 | User query error |



### 四，购物车页面商品增加

**URL：**`127.0.0.1:8000/v1/carts/<username>`

**请求方式：**PUT

**请求参数：**JSON

|  参数  | 类型 | 是否必须 |      说明      |
| :----: | :--: | :------: | :------------: |
| sku_id | int  |    是    |   商品sku_id   |
| count  | int  |    是    | 前端显示的数量 |
| state  | str  |    是    |  判断事件状态  |

```python
#请求示例
{'sku_id':1001,count:1,state:'add'}
```

**返回值**：JSON

**响应格式：**

```python
#响应示例：
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                        |
| ----- | -------- | ---- | --------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码 |
| data  | 具体数据 | dict | 与error二选一               |
| error | 错误信息 | char | 与data二选一                |

**skus_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
|  sku_sale_atr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```

**状态码参考**

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30101  | 未找到商品 | SKU query error  |
| 30104  | 未找到用户 | User query error |



### 五，购物车页面商品减少

**URL**：`127.0.0.1:8000/v1/carts/<username>`

**请求方式:** PUT

**请求参数：**JSON

|  参数  | 类型 | 是否必须 |     说明     |
| :----: | :--: | :------: | :----------: |
| sku_id | int  |    是    | 商品的sku_id |
| count  | int  |    是    | 前端显示数量 |
| state  | str  |    是    | 判断事件状态 |

```python
#请求示例：
{'sku_id':1001,count:1,state:'del'}
```

**返回值：**JSON

**响应格式：**

```python
#响应示例：
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                        |
| ----- | -------- | ---- | --------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码 |
| data  | 具体数据 | dict | 与error二选一               |
| error | 错误信息 | char | 与data二选一                |

**skus_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
| sku_sale_attr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```

**状态码参考**

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30101  | 未找到商品 | SKU query error  |
| 30104  | 未找到用户 | User query error |



### 六，购物车商品选择勾选

**URL**：`127.0.0.1:8000/v1/carts/<username>`

**请求方式:** PUT

**请求参数：**JSON

|  参数  | 类型 | 是否必须 |          说明          |
| :----: | :--: | :------: | :--------------------: |
| sku_id | int  |    是    | 购物车显示商品的sku_id |
| state  | str  |    是    |      判断事件状态      |

```python
#请求示例
{'sku_id':1001,state:'select'}
```

**返回值：**JSON

**响应格式：**

```python
#响应示例：
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                            |
| ----- | -------- | ---- | ------------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码参考 |
| data  | 具体数据 | dict | 与error二选一                   |
| error | 错误信息 | char | 与data二选一                    |

**skus_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
| sku_sale_attr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```

**状态码参考**

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30101  | 未找到商品 | SKU query error  |
| 30104  | 未找到用户 | User query error |



### 七，购物车商品取消勾选

**URL**：`127.0.0.1:8000/v1/carts/<username>`

**请求方式:** PUT

**请求参数：**JSON

|  参数  | 类型 | 是否必须 |          说明          |
| :----: | :--: | :------: | :--------------------: |
| sku_id | int  |    是    | 购物车显示商品的sku_id |
| state  | str  |    是    |      判断事件状态      |

```python
#请求示例
{'sku_id':1001,state:'unselect'}
```



**返回值:**JSON

**响应格式：**

```python
#响应示例：
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                            |
| ----- | -------- | ---- | ------------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码参考 |
| data  | 具体数据 | dict | 与error二选一                   |
| error | 错误信息 | char | 与data二选一                    |

**skus_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
| sku_sale_attr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```

**状态码参考**

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30101  | 未找到商品 | SKU query error  |
| 30104  | 未找到用户 | User query error |



### 八，购物车商品全选

**URL**：`127.0.0.1:8000/v1/carts/<username>`

**请求方式:** PUT

**请求参数：**JSON

|  参数  | 类型 | 是否必须 |            说明            |
| :----: | :--: | :------: | :------------------------: |
| sku_id | list |    是    | 购物车显示商品所有的sku_id |
| state  | str  |    是    |        判断事件状态        |

```python
#请求示例：
{'sku_id':[1001,1002,1003,...],state:'selectall'}
```

**返回值：**JSON

**响应格式：**

```python
#响应示例：
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                            |
| ----- | -------- | ---- | ------------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码参考 |
| data  | 具体数据 | dict | 与error二选一                   |
| error | 错误信息 | char | 与data二选一                    |

**skus_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
| sku_sale_attr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```

**状态码参考**

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30104  | 未找到用户 | User query error |



### 九，购物车商品全不选

**URL**：`127.0.0.1:8000/v1/carts/<username>`

**请求方式:** PUT

**请求参数：**JSON

|  参数  | 类型 | 是否必须 |            说明            |
| :----: | :--: | :------: | :------------------------: |
| sku_id | list |    是    | 购物车显示商品所有的sku_id |
| state  | str  |    是    |        判断事件状态        |

```python
#请求示例
{'sku_id':[1001,1002,1003,...],state:'unselectall'}
```



**返回值：**JSON

**响应格式：**

```python
#响应示例：
{"code":200,"data":skus_list}
```

| 字段  | 含义     | 类型 | 备注                            |
| ----- | -------- | ---- | ------------------------------- |
| code  | 状态码   | int  | 默认正常为200，异常见状态码参考 |
| data  | 具体数据 | dict | 与error二选一                   |
| error | 错误信息 | char | 与data二选一                    |

**skus_list参数信息**

|        参数        |  类型   | 是否必须 |               说明               |
| :----------------: | :-----: | :------: | :------------------------------: |
|         id         |   int   |    是    |            商品sku_id            |
|        name        |   str   |    是    |             商品名称             |
|       count        |   int   |    是    |             商品数量             |
| default_image_url  |   str   |    是    |         商品默认图片路径         |
|       price        | decimal |    是    |             商品单价             |
| sku_sale_attr_name |  list   |    是    |             商品属性             |
| sku_sale_attr_val  |  list   |    是    |            商品属性值            |
|      selected      |   int   |    是    | 商品的选中状态（0未选中，1选中） |

```python
#sku_list中数据示例
[{"id":"","name":"","count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
```

 **状态码参考**

| 状态码 | 响应信息   | 原因短语         |
| ------ | ---------- | ---------------- |
| 200    | 正常       | OK               |
| 30104  | 未找到用户 | User query error |

