package com.dingdong.client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.security.MessageDigest;

public class DingDongClient{

    public static final String SECRET_KEY = "dingdong_abc@@123"; //密钥
    public static final String SPLIT_FLAG = "____@@@____"; //分隔符
    public static final String SERVER_HOST = "127.0.0.1"; //主机host
    public static final int SERVER_PORT = 1234; //主机端口

    /*
     * 根据指令及指令参数生成发送的数据
     * @param opt 指令
     * @param optParams 指令参数
     * @return String 返回加密的数据
     */
    public static String genDatas(String opt, String params){
        String timestamp = "" + System.currentTimeMillis() / 1000;
        String tokenSrc = String.join("|", new String[]{opt, params, timestamp, SECRET_KEY});
        String token = MD5(tokenSrc);
        return String.join(SPLIT_FLAG, new String[]{opt, params, timestamp, token.toLowerCase()});
    }
    private static String MD5(String s) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] bytes = md.digest((s).getBytes("utf-8"));
            return toHex(bytes);
        }
        catch (Exception e) {
            return "";
        }
    }
    private static String toHex(byte[] bytes) {
        final char[] HEX_DIGITS = "0123456789ABCDEF".toCharArray();
        StringBuilder ret = new StringBuilder(bytes.length * 2);
        for (int i=0; i<bytes.length; i++) {
            ret.append(HEX_DIGITS[(bytes[i] >> 4) & 0x0f]);
            ret.append(HEX_DIGITS[bytes[i] & 0x0f]);
        }
        return ret.toString();
    }

    /*
     * 程序入口
     */
    public static void main(String[] args) throws IOException {
        //获取指令
        String opt = "";
        if(args.length >= 1){
            opt = args[0];
        }

        //获取指令参数
        String optParams = "";
        if(args.length >= 2){
            optParams = args[1];
        }

        //建立socket连接并发送数据
        Socket socket = new Socket();
        socket.connect(new InetSocketAddress(SERVER_HOST, SERVER_PORT), 5000);
        PrintWriter out = new PrintWriter(socket.getOutputStream());
        out.print(genDatas(opt, optParams)+"\r\n");
        out.flush();
        System.out.println(" client send: opt=" + opt + "&optParams," + optParams);

        //接收数据
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        String info = null;
        while((info=reader.readLine()) != null){
            System.out.println("Received from server:" + info);
        }

        //关闭连接
        out.close();
        socket.close();
    }

}
