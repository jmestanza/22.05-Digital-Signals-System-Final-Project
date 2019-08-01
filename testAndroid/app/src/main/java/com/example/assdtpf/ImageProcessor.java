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
import android.util.Pair;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.*;
import org.opencv.imgproc.Imgproc;
import org.opencv.android.Utils;

import java.util.ArrayList;
import java.util.List;

import static java.lang.Math.abs;

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
    private Mat confidence, shapeMask, grey_scale; // matriz de confianza
    private Mat sobel_x, sobel_y; // espacio para derivadas
    private List<Pair<Integer,Integer>> square; // cuadrado de busqueda

    public ImageProcessor(Context ctx){
        OpenCVLoader.initDebug();

        img = null;
        flooded = null;
        this.ctx = ctx;

        search_square_size = ctx.getResources().getInteger(R.integer.search_square_size);
        search_times = ctx.getResources().getInteger(R.integer.search_times);
        square_size = ctx.getResources().getInteger(R.integer.square_size);

        lower = new Scalar(15,15,15);
        upper = new Scalar(100,100,100);


    }
    public void setBitmap(Bitmap bitmap){
        if (img == null){
            img = new Mat();
        }

        this.bitmap = bitmap;
        Bitmap bmp32 = bitmap.copy(Bitmap.Config.ARGB_8888, true);
        Utils.bitmapToMat(bmp32, img);

        /** Matrices necesarias para el algoritmo **/
        confidence = new Mat(
                img.size(),
                CvType.CV_32SC1
        );

        shapeMask = new Mat(
                img.size(),
                CvType.CV_32SC1
        );

        sobel_x = new Mat();
        sobel_y = new Mat();

        grey_scale = new Mat();

        square = new ArrayList<Pair<Integer,Integer>>();

        for (int i = 0;i < square_size;i++){
            for (int j = 0;j < square_size;j++){
                square.add(new Pair<>(
                        i - square_size / 2,
                        j - square_size / 2
                ));
            }
        }
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

        Core.inRange(flooded, lower, upper,shapeMask);

        Mat hierarchy = new Mat();
        Imgproc.findContours(shapeMask.clone(), points, hierarchy, Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
        hierarchy.release();

        /// Buscamos el mejor beneficio
        Float best_benefit = 0f;
        Integer best_benefit_point = null;

        Imgproc.cvtColor(img, grey_scale, Imgproc.COLOR_BGR2GRAY);

        Imgproc.Sobel(grey_scale, sobel_y, 5, 1, 0);
        Imgproc.Sobel(grey_scale, sobel_x, 5, 0, 1);

        Core.multiply(sobel_x, new Scalar(-1), sobel_x);


        for (MatOfPoint contorno : points){ // por cada contorno distinto

            List<Point> border_normal = new ArrayList<>(); // normales al borde
            Point []local_points = contorno.toArray();
            int n = local_points.length;

            for (int i = 0;i < n;i++){
                double dx = local_points[i].x - local_points[(i-1)%n].x;
                double dy = local_points[i].y - local_points[(i-1)%n].y;

                border_normal.add(new Point(dy, -dx));
            }

            int index = 0;

            for (Point border_point : local_points){
                int x = (int)border_point.x;
                int y = (int)border_point.y;

                double sum_confidence = 0;

                for (Pair<Integer,Integer> dd : square) {
                    int dy = dd.first;
                    int dx = dd.second;
                    double []v = shapeMask.get(y + dy, x + dx);

                    if (v[0] < 0.1f){
                        // fuera de la zona a retocar
                        sum_confidence += confidence.get(y + dy, x + dx)[0];
                    }
                }
                sum_confidence /= square.size();
                double nx = border_normal.get(index).x;
                double ny = border_normal.get(index).y;

                float max_grad = 0f;
                Pair<Float,Float> max_grad_value = new Pair<>(0f,0f);

                for (Pair<Integer,Integer> dd : square){
                    int dy = dd.first;
                    int dx = dd.second;
                    double []v = shapeMask.get(y + dy, x + dx);

                    if (v[0] < 0.1f){



                    }
                }

                index ++;
            }

        }

        Log.d("ImageEditLogs","Contorno encontrado");

    }
}
