package com.example.assdtpf;

import android.app.Activity;
import android.util.Log;

public class ThreadProcess extends Thread{ // esta clase simplifica el uso de threads
    ThreadListener listener;
    Long iterations;
    boolean end;
    public ThreadProcess(){
        iterations = 0l;
        end = false;
    }
    public void run(){
        end = false;
        boolean cont = true;
        while (cont && !end){
            //Log.d("ImageEditLogs","Running iteration "+iterations);
            cont = this.listener.runThread();
            iterations ++; // mientras retorna true seguimos
        }
        finish();
    }
    public void finish(){
        end = true;
        if (this.listener != null){
            this.listener.threadFinish();
        }
    }
    public ThreadListener getListener() {
        return listener;
    }

    public void setListener(ThreadListener listener) {
        this.listener = listener;
    }

}
