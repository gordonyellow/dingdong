package com.dingdong;

import android.app.Activity;
import android.app.AlertDialog;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.EditText;
import android.content.Context;
import android.content.DialogInterface;
import android.text.TextUtils;
import android.util.Log;
import java.util.List;
import java.util.ArrayList;
import java.io.*;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.security.MessageDigest;
import com.dingdong.util.ToastUtil;


public class DingDongAndroidClient extends Activity{

    public static final String SECRET_KEY = "dingdong_abc@@123"; //密钥
    public static final String SPLIT_FLAG = "____@@@____"; //分隔符
    public static final String SERVER_HOST = "127.0.0.1"; //主机host
    public static final int SERVER_PORT = 1234; //主机端口
    private static final String TAG = DingDongAndroidClient.class.getName();
    private static final String FILE_PATH = "/mnt/sdcard/netease/cloudmusic/Music/任月丽 - 天使的翅膀.mp3";

    private TextView cmdTextView;
    private EditText msgEditText;
    private Context ctx;

    private Socket socket;
    private BufferedReader in;
    private PrintWriter out;

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        ctx = DingDongAndroidClient.this;

        cmdTextView = (TextView) this.findViewById(R.id.cmdTextView);
        msgEditText = (EditText) this.findViewById(R.id.msgEditText);

        final List<Object[]> cmdInfoList = new ArrayList<Object[]>();
        cmdInfoList.add(new Object[] { "PlayMusic", "播放音乐" });
        cmdInfoList.add(new Object[] { "StopPlayMusic", "停止播放音乐" });
        cmdInfoList.add(new Object[] { "SaySth", "播放文字" });
        cmdInfoList.add(new Object[] { "StopSaySth", "停止播放文字" });
        cmdInfoList.add(new Object[] { "PlayVoice", "播放声音文件" });
        cmdInfoList.add(new Object[] { "StopPlayVoice", "停止播放声音文件" });

        final String[] cmdItems = new String[cmdInfoList.size()];
        for (int i = 0; i < cmdInfoList.size(); i++) {
            cmdItems[i] = (String) cmdInfoList.get(i)[1];
        }

        try{
            socket = new Socket(SERVER_HOST, SERVER_PORT);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
        }catch(IOException ex){
            ex.printStackTrace();
        }

        findViewById(R.id.chooseCmdBtn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                new AlertDialog.Builder(ctx).setTitle("请点击选择")
                        .setItems(cmdItems, new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface arg0, int arg1) {
                                cmdTextView.setText(cmdItems[arg1]);
                                cmdTextView.setTag(cmdInfoList.get(arg1)[0]);
                            }
                        }).show();
            }
        });

        findViewById(R.id.sendCmdBtn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0){
                try{
                    //发送数据
                    String opt = (String)cmdTextView.getTag();
                    String optParams = "";
                    if("SaySth".equals(opt)){
                        optParams = msgEditText.getText().toString();
                    }
                    if("PlayVoice".equals(opt)){
                        optParams = "size=" + new File(FILE_PATH).length() + "&type=mp3";
                    }
                    Log.d(TAG, "opt=" + opt + " & optParams=" + optParams);
                    if (socket.isConnected()) {
                        if (!socket.isOutputShutdown()) {
                            out.println(genDatas(opt, optParams));
                            out.flush();
                            Log.d(TAG, "client send: opt=" + opt + " & optParams=" + optParams);

                            if("PlayVoice".equals(opt)){
                                DataInputStream fis = new DataInputStream(
                                    new BufferedInputStream(new FileInputStream(FILE_PATH)));
                                DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
                                int bufferSize = 8192;
                                byte[] buf = new byte[bufferSize];
                                while(true){
                                    int read = 0;
                                    if (fis != null) {
                                        read = fis.read(buf);
                                    }
                                    if (read == -1) {
                                        break;
                                    }
                                    dos.write(buf,0,read);
                                }
                                dos.flush();
                            }
                        }else{
                            Log.d(TAG, "socket output shutdowned");
                        }
                    }else{
                        Log.d(TAG, "socket not connected");
                    }

                    //接收数据
                    /*
                    BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    String info = null;
                    while((info=reader.readLine()) != null){
                        Log.d(TAG, "Received from server:" + info);
                        ToastUtil.showMessage(ctx, info);
                    }
                    */

                    //关闭连接
                    //out.close();
                    //socket.close();
                }catch(Exception e){
                    System.out.println(e);
                    ToastUtil.showMessage(ctx, e.getMessage());
                }
            }
        });
    }

    /*
     * 根据指令及指令参数生成发送的数据
     * @param opt 指令
     * @param optParams 指令参数
     * @return String 返回加密的数据
     */
    private static String genDatas(String opt, String params){
        String timestamp = "" + System.currentTimeMillis() / 1000;
        String tokenSrc = TextUtils.join("|", new String[]{opt, params, timestamp, SECRET_KEY});
        String token = MD5(tokenSrc);
        return TextUtils.join(SPLIT_FLAG, new String[]{opt, params, timestamp, token.toLowerCase()});
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
}
