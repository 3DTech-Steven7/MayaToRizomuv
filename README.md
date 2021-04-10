## MayaToRizomUV是什么?
这是一个能实时在RizomUV与Maya间分UV的工具。

## Features - 特性

* 方便的`交互式分UV`功能
* 工具省去相互导入导出的操作，`快捷高效`
* 编辑和预览`同步`，所见即所得
* 模型只需保存即可自动化传递UV，`制作效率高错误几率小`
* 强大的`自动化分UV`功能，快速实现效果
* 实时操作修改模型UV，`交互效率高`
* 完美兼容`Maya2014-Maya2022+`多版本
* 具有多项传递、选择边线等功能，`功能丰富强大`
* 快捷的`一键式`安装的插件

## Installation - 安装
#### 自动安装
1. 点击MayaToRizomUV文件夹中的install_modules.cmd进行安装
2. 出现Install Successful表示安装成功
3. 重开Maya后找到在Windows-Setting/Perferences中的Plug-in Manager，搜索MayaToRizomuv.py插件点击Loaded进行使用

#### 手动安装
1. 点击MayaToRizomUV文件夹中的install_modules.cmd进行安装
2. 在MayaToRizomUV文件夹中找到modules文件夹，复制到我的文档中Maya文件夹下
3. 重开Maya后找到在Windows-Setting/Perferences中的Plug-in Manager，搜索MayaToRizomuv.py插件点击Loaded进行使用

## Usage - 用法
###### 具体在B站搜索mayatorizomuv
### 第一次使用
1. 点击Edit-Preferences
2. 点击...打开RizomUV.exe启动文件选择
3. 设置完毕后点击Ok
4. * 可以直接点击Send Link
   * 如果想快速的话可以直接点Push或者自动化功能，会弹出是否启动程序，选是即可
5. 点击后启动程序即可分UV
6. 在需要传回maya时点击Pull即可

### UVTool
1. 使用AutoCut可以自动切割模型UVShell，如果在Selection Mode的模式下则是在选择的Shell中切割

### MayaTool
##### Select Similar
* 选择相同的物体
 
##### Transfer SectionUV
* 对选择的物体进行UV传递，仅作用于相同拓扑###Select Similar

##### LiveLink
* 开启即可使用实时分UV

##### Scrpit
* 可以使用自定义脚本进行自动化处理
如fullAuto("pSphere*")
参照maya的cmd的语法使用


## Changelog - 更新日志
###### V2021.4.10.02 版本内容更新
* 更新支持Maya2022,并且向下兼容至Maya2014
* 实时链接LiveLink功能优化，提高稳定性
* 修复存在命名相同物体无法传递的BUG
* 修复使用中文无法通过功能按钮启动链接的BUG
* 标准安装目录下第一次使用无需创建modules文件夹，实现一键式安装
* 优化改进标准功能的传递功能
* 优化Node传递逻辑,交互速度提升30%
* 汉化Log提示内容

## Issue - 已知问题
* 不支持Zbrush Goz到Maya的物体进行修改UV
* Maya2014单击传递无效，需要二次点击传递
* RizomUV2018版自动化功能部分不兼容
* 部分非标准节点模型传递会变形
* Maya2022使用LiveLink有几率崩溃

## Contact - 联系
在使用中有任何问题，欢迎反馈给我，可以用以下联系方式跟我交流

* 邮件(32229170@qq.com)
* 微信公众号(3DTech)
* QQ技术交流群: 76031183

## Dos - 文档
* 最新更新:https://www.jianshu.com/p/d82f2b21b05a
* 用户帮助:https://www.jianshu.com/p/000663862bec
* 工具演示:https://www.jianshu.com/p/bcbdc83c1a65

## Donor developer - 捐助开发者
在兴趣的驱动下,写一个`免费`的东西，有欣喜，也还有汗水，希望你喜欢我的作品，同时也能支持一下。

## Authors and acknowledgment - 贡献者和感谢
感谢以下,排名不分先后

* 余则成
* 刘超
* chenclean
* The dead is comin
* 香蕉橘子西瓜汁
* 北海公瑾
* 金王斌

## License - 版权信息
该项目签署了GNU General Public License v3.0 授权许可，详情请参阅 LICENSE.md
### 关于作者
Steven7
