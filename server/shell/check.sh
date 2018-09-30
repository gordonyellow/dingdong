BASE_PATH=$(cd `dirname $0`; pwd) #获取当前脚本文件所在目录
. $BASE_PATH/common.sh #加载相关变量
pid=`ps -ef|grep -v grep|grep "${PYTHON_PATH}"|grep "${DING_DONG_PATH}"|awk '{print $2}'`
if [ "$pid" = "" ]; then
    echo "服务未启动"
    sh $BASE_PATH/start.sh
else
  echo "服务已启动...,pid=${pid}"
fi
