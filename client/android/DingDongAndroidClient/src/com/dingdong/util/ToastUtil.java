package com.dingdong.util;

import android.content.Context;
import android.widget.Toast;

/**
 * Toast工具类 
 */
public class ToastUtil {
    private static Toast toast = null;
    public static int LENGTH_LONG = Toast.LENGTH_LONG;
    public static int LENGTH_SHORT = Toast.LENGTH_SHORT;

    /**
     * Toast发送消息，默认Toast.LENGTH_SHORT 
     * @param act
     * @param msg
     */
    public static void showMessage(final Context act, final String msg) {
        showMessage(act, msg, LENGTH_SHORT);
    }

    /**
     * Toast发送消息，默认Toast.LENGTH_LONG 
     * @param act
     * @param msg
     */
    public static void showMessageLong(final Context act, final String msg) {
        showMessage(act, msg, LENGTH_LONG);
    }

    /**
     * Toast发送消息 
     * @param act
     * @param msg
     * @param len
     */
    public static void showMessage(final Context act, final int msg,
                                   final int len) {

        if (toast != null) {
            toast.setView(toast.getView());
            toast.setText(msg);
            toast.setDuration(len);
        } else {
            toast = Toast.makeText(act, msg, len);
        }
        toast.show();

    }

    /**
     * Toast发送消息 
     * @param act
     * @param msg
     * @param len
     */
    public static void showMessage(final Context act, final String msg,
                                   final int len) {
    if (toast != null) {
        toast.setView(toast.getView());
        toast.setText(msg);
        toast.setDuration(len);
    } else {
        toast = Toast.makeText(act, msg, len);
    }
    toast.show();

    }

    /**
     * 关闭当前Toast 
     */
    public static void cancelCurrentToast() {
        if (toast != null) {
            toast.cancel();
        }
    }
}  
