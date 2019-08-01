/*** Flood fill
 * https://github.com/JavaOpenCVBook/code/blob/master/chapter3/floodfill/src/main/java/org/javaopencvbook/utils/FloodFillFacade.java
 **/

/** https://github.com/JavaOpenCVBook/code/blob/master/chapter3/floodfill/src/main/java/org/javaopencvbook/GUI.java
 *
 */

/** https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html#floodfill
 *
 */
package com.example.assdtpf;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Path;
import android.media.Image;
import android.util.Log;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.*;
import org.opencv.imgproc.Imgproc;
import org.opencv.android.Utils;

import java.util.ArrayList;
import java.util.List;

public class ImageProcessor {
    private Bitmap bitmap;
    private Mat flooded;
    private Mat img;

    private Bitmap pathBitmap;
    private Context ctx;

    private Integer search_square_size;
    private Integer search_times;
    private Integer square_size;

    private Scalar lower, upper;
    private Mat confidence, shapeMask; // matriz de confianza

    public ImageProcessor(Context ctx){
        OpenCVLoader.initDebug();

        img = null;
        flooded = null;
        this.ctx = ctx;

        search_square_size = ctx.getResources().getInteger(R.integer.search_square_size);
        search_times = ctx.getResources().getInteger(R.integer.search_times);
        square_size = ctx.getResources().getInteger(R.integer.square_size);

        lower = new Scalar(0,0,0);
        upper = new Scalar(15,15,15);


    }
    public void setBitmap(Bitmap bitmap){
        if (img == null){
            img = new Mat();
        }

        this.bitmap = bitmap;
        Bitmap bmp32 = bitmap.copy(Bitmap.Config.ARGB_8888, true);
        Utils.bitmapToMat(bmp32, img);

        confidence = new Mat(
                img.size(),
                CvType.CV_8SC4
        );

        shapeMask = new Mat(
                img.size(),
                CvType.CV_8SC4
        );
    }
    public void setPath(Bitmap bitmap){
        this.pathBitmap = bitmap;
    }
    public void computeContours(){
        //List<MatOfPoint> contours = new ArrayList<MatOfPoint>();

        /*Imgproc.findContours(
                img, contours, new Mat(), Imgproc.RETR_LIST, Imgproc.CHAIN_APPROX_SIMPLE
        );*/

        Mat mask = new Mat();
        Mat inputMatSmall = new Mat();
        Mat inputMat = new Mat();
        Mat grayImage = new Mat();

        Bitmap bmp32 = pathBitmap.copy(Bitmap.Config.ARGB_8888, true);
        Utils.bitmapToMat(bmp32, inputMatSmall);

        Size sz = new Size(bitmap.getWidth(),bitmap.getHeight());
        Imgproc.resize( inputMatSmall, grayImage, sz );

        Imgproc.cvtColor(grayImage, inputMat, Imgproc.COLOR_BGR2GRAY);

        Imgproc.floodFill(
                inputMat,
                mask,
                new Point(1,1),
                new Scalar(0, 0, 0),
                new Rect(),
                new Scalar(255,255,255),
                new Scalar(0,0,0),
                4
        );

        flooded = inputMat;
    }
    public Bitmap getFloodedBitmap(){
        Bitmap outputBitmap = Bitmap.createBitmap(
                bitmap.getWidth(),
                bitmap.getHeight(),
                Bitmap.Config.ARGB_8888
        );

        Utils.matToBitmap(flooded, outputBitmap);
        return outputBitmap;
    }

    public void runIteration() {
        /// correr una iteración del algoritmo


        /// buscamos contornos
        List<MatOfPoint> points = new ArrayList<>();

        Imgproc.findContours(shapeMask.clone(), points, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_NONE);
        Imgproc.find
        Log.d("ImageEditLogs","Contorno encontrado");

    }
}
