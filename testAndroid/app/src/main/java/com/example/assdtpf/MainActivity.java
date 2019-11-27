package com.example.assdtpf;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;
import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.*;
import org.opencv.imgproc.Imgproc;

public class MainActivity extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {
    Mat mRgba;
    Mat mRgbaF;
    Mat mRgbaT;
    Mat mRgbaW;
    Mat darkBackground;

    CameraBridgeViewBase camera;
    BaseLoaderCallback baseLoaderCallback;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        camera = findViewById(R.id.myCameraView);

        camera.setVisibility(View.VISIBLE);

        camera.setCvCameraViewListener(this);

        //camera.enableView();
        baseLoaderCallback = new BaseLoaderCallback(this) {
            @Override
            public void onManagerConnected(int status) {
                super.onManagerConnected(status);

                switch(status){

                    case BaseLoaderCallback.SUCCESS:
                        camera.enableView();
                        break;
                    default:
                        super.onManagerConnected(status);
                        break;
                }
            }
        };
    }

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
        mRgba = inputFrame.rgba();
        Core.transpose(mRgba, mRgbaT);

        return mRgba;
    }

    @Override
    public void onCameraViewStarted(int width, int height) {
        Log.d("ImageEditLogs","width="+width+", height="+height);

        camera.enableView();
        darkBackground = new Mat(height, width, CvType.CV_8UC4);
        mRgba = new Mat(height, width, CvType.CV_8UC4);
        mRgbaF = new Mat(height, width, CvType.CV_8UC4);
        mRgbaT = new Mat(width, height, CvType.CV_8UC4);
        mRgbaW = new Mat(height, width, CvType.CV_8UC4);
    }

    @Override
    public void onCameraViewStopped() {
        mRgba.release();
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (camera != null){
            camera.disableView();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (!OpenCVLoader.initDebug()){
            Log.d("CVTestLogs","There is a problem in openCV");
        }else{
            Log.d("CVTestLogs","OpenCV loaded");
            baseLoaderCallback.onManagerConnected(baseLoaderCallback.SUCCESS);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (camera!=null){
            camera.disableView();
        }
    }
}
