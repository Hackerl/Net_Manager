软件管理平台
==========
    数据库
        |
         -----  auth表，储存合法订单号
                    |
                     -----  订单尾号 | 服务期限 | 已付金额 | 允许验证次数 |  验证成功的用户名 | 验证成功的mac地址
        |
         -----  application表，存储应用信息
                    |
                     -----   应用名  | 最新版本 | 更新日志 | 下载地址
    |

    网站主体
        |
         -----  授权api[Authorization]：获取用户发送的订单后8位，手机Mac地址，用户名，调用 manage.Authorization　，返回认证结果
        |
         -----  更新api[Update]：获取用户发来的软件名称，版本信息，调用 manage.Update(app名)，返回是否有新版本，更新日志，以及新版本下载地址
        |
         -----  管理api[manage]：网站后台，发布更新消息，查看授权状态，用户数据
                    |
                     -----  发布更新api[set_application]，调用 Info.set_app_info(程序名　，版本号　，更新日志　，下载地址)，为数据库中的该程序条目设置新版本信息
                    |
                     -----  查询信息api[get_all_information]，调用 Info.get_information()，获取当前所有信息，包括用户授权状况，app版本情况
                    |
                     -----  添加认证信息api[add_new_auth]，获取管理员post的 [订单号 | 服务时间　｜　金额] ，调用 Info.add_auth_status(新的订单号 ， 服务时间　，　金额) 向数据库里写入合法订单号

    manage类
        |
         -----  Authorization：调用 Info.auth(订单后8位)，取得数据库信息对比，返回是否是合法用户
                    |
                     -----  如果合法，将用户post上来的 用户名，服务期限，以及数据库中查询到的用户购买的服务期限(例如，一个月期限)，加密后返回加密后信息，作为登录凭证
                                |
                                 ----- 调用 Info.set_auth_status(订单尾号，用户名，mac地址)为认证后的条目更新信息
        |
         -----  Update：调用 Info.get_version(程序名)，从数据库中获取查询 程序 的最新版本，与用户发送来的版本信息对比
                    |
                     ----- 如果可更新，返回更新信息，更新日志，下载地址

    Info类
        |
         -----  auth：根据传入的订单号，去数据库中查询合法的订单号，以及是否验证过，进行对比，返回 true/false
        |
         -----  set_auth_status：验证成功后，会调用此方法，更新条目，防止多次认证
        |
         -----  add_auth_status：添加订单尾号条目
        |
         -----  get_version：根据传入的程序名，去数据库中查询该程序的最新信息，如版本号、更新日志、下载地址，返回 信息的List
        |
         -----  get_information：获取所有表格信息，并返回


加密方式：
    用户发送来的所有信息都会被加密，使用软件中硬编码的秘钥，防止被抓包
    manage.Authorization　调用Info.auth(订单号)，认证成功后，生成随机字符串，将post得到的 订单尾号 用户名 以及数据库中储存的服务期限 用此随机字符串做秘钥加密，然后将此随机字符串用mac加密，放在密文的中间，返回给客户端
    客户端接受密文，用 Mac + 公共秘钥 的散列值作为文件名，储存这个文件
    客户端使用时，对于app，可以从SharedPreferences中获取，不必每次都查询wifi的物理地址，获取Mac后，和公共秘钥做散列，查询目录下有无此文件
    如果有，从密文中间提取随机字符串的加密密文，用Mac作为秘钥解码，获取秘钥，在用此解码剩下密文，获得 用户名 | 服务期限，如果当前要拨号的用户名和这个用户名相同，以及服务期限未到，允许拨号
    
破解方式：
    逆向得到算法，然后模拟生成登录凭证，为每一台手机，生成特定mac地址的登录凭证，然后放到app文件夹下
    逆向app，更改逻辑，跳过验证，直接拨号




