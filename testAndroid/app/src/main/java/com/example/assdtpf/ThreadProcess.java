package com.example.assdtpf;

import android.util.Log;

public class ThreadProcess extends Thread{
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
    }
    public void finish(){
        end = true;
    }
    public ThreadListener getListener() {
        return listener;
    }

    public void setListener(ThreadListener listener) {
        this.listener = listener;
    }
}
