package com.example.assdtpf;

import android.graphics.Bitmap;
import android.graphics.Path;
import android.media.Image;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.imgproc.Imgproc;
import org.opencv.android.Utils;

import java.util.ArrayList;
import java.util.List;

public class ImageProcessor {
    private Bitmap bitmap;
    private Mat img;

    private Path path;

    public ImageProcessor(){

    }
    public void setBitmap(Bitmap bitmap){
        this.bitmap = bitmap;
        Bitmap bmp32 = bitmap.copy(Bitmap.Config.ARGB_8888, true);
        Utils.bitmapToMat(bmp32, img);
    }
    public void setPath(Path path){
        this.path = path;
    }
    public void computeContours(){
        List<MatOfPoint> contours = new ArrayList<MatOfPoint>();

        /*Imgproc.findContours(
                img, contours, new Mat(), Imgproc.RETR_LIST, Imgproc.CHAIN_APPROX_SIMPLE
        );*/
        Imgproc.floodFill(myMat2, flooded, flood, new Scalar(255, 255, 255), new Rect(), lowerDiff, upperDiff, 4);
         
    }
}
