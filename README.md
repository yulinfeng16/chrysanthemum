# chrysanthemum
一个简单的Python程序，和sdwebui-api-manager一起使用可以通过简单的api唤起Stable Diffusion生成春节风格儿童头像。
# 环境配置
此项目需要：[sdwebui-api-manager](https://github.com/nftblackmagic/sdwebui-api-manager)先运行。该部分配置教程可以转到sdwebui-api-manager的主页。

假定您已经成功运行了以上项目，您应该可以访问localhost:5001/docs。此时可以开始配置该项目。

此项目主体仅一个python脚本，通过flask提供服务。因此，您需要在控制台：
`
pip install Flask-Cors
`。
之后运行脚本即可。

脚本无需和sdwebui-api-manager放在同一目录。
# API调用
完成环境配置后，向localhost:18888/process_image发送一个POST以调用API。这个POST应该带有一个JSON，内容格式：
```
{

"img_base64":"这里填你要向Stable Diffusion的Roop插件中传入的人脸图片的base64格式",

"ismale":"填1个数字，0代表生成女孩头像，1代表生成男孩头像"

}
```
之后会自动生成图片，实测需要1分钟左右。
# 修改参数
代码的send()函数中有两处data={...}内容，大概在十几行的位置开始。修改里面的参数即可，像调用原来的StableDiffusionAPI一样。
