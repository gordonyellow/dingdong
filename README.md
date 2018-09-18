# 项目名称
dingdong提醒
# 背景介绍
因为爸妈经常不把手机带身上，导致我在外面想打电话找他们的时候电话一直没人接，但其实他们基本整天在家的，而家里大厅里面基本上一直开着一台mac mini（方便随时工作或者鼓捣代码），所以萌生了这个项目的想法，就是可以在外面通过手机之类的方式给mac mini发指令，让mac mini发出声音提醒，这样子就不必担心他们没带手机在身边了。
# 实现功能
初期很简单，就是在微信上发一个1，然后让mac mini播放一首歌，后来又做了在微信上发送文字，然后在mac mini上将文字转成声音播放出来的功能，再后来又把微信端发送语音消息，然后在mac mini端播放也一起做了。<br/>
# 技术实现
* 用python写了一个简单的socket server服务端接受请求；
* 在服务端中调用mac操作系统自带的say命令进行文字转语音，调用afplay命令进行音乐播放；
* 因为需要由微信端向mac mini端发起请求，所以微信端需要在公网上定位到mac mini，申请了一个免费的花生壳域名在路由中设置了ddns，使得微信端可以在公网通过花生壳域名访问到路由，再在路由设置了转发处理，将微信端的请求通过路由转发给mac mini,这样子就实现了微信端与mac mini的通信。
# 目录结构
* server--服务端代码
* client--客户端代码
* client/python---python客户端代码
* client/java-----java客户端代码
* client/android--安卓客户端代码
# 运行
* 服务端启动 sh server/shell/start.sh
* 服务端关闭 sh server/shell/stop.sh
* 服务端重启 sh server/shell/restart.sh
* python客户端运行
   * cd client/python
   * python3 DingDongClient.py PlayMusicThread
* java客户端运行   
   * cd client/java/src  
   * javac com/dingdong/client/DingDongClient.java 
   * java com.dingdong.client.DingDongClient PlayMusicThread
