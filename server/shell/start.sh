BASE_PATH=$(cd `dirname $0`; pwd) #获取当前脚本文件所在目录
#echo BASE_PATH=$BASE_PATH

. $BASE_PATH/common.sh #加载相关变量
#echo PYTHON_PATH=${PYTHON_PATH}
#echo DING_DONG_PATH=${DING_DONG_PATH}

#############
#检验是否已启动服务
#############
pid=`ps -ef|grep -v grep|grep "${PYTHON_PATH}"|grep "${DING_DONG_PATH}"|awk '{print $2}'`
if [ ! $pid ]; then
  echo "开始启动..."
  $($PYTHON_PATH $DING_DONG_PATH >/dev/null 2>&1 &)  #启动服务
else
  echo "服务已启动 pid=$pid"
  exit 0 #退出脚本执行
fi

#############
#打印启动结果到终端
#############
pid=`ps -ef|grep -v grep|grep "${PYTHON_PATH}"|grep "${DING_DONG_PATH}"|awk '{print $2}'`
if [ ! $pid ]; then
  echo "启动失败"
else
  echo "启动成功 pid=$pid"
fi
