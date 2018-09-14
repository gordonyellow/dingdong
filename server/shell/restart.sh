BASE_PATH=$(cd `dirname $0`; pwd) #获取当前脚本文件所在目录
sh ${BASE_PATH}/stop.sh && sh ${BASE_PATH}/start.sh
