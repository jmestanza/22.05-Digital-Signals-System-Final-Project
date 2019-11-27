/*** Image processor: by Ariel Nowik
 * Este código se encarga de realizar todo el procesamiento de imagenes del programa utilizando la
 * libería openCV
 *
 */


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
import android.view.WindowId;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.*;
import org.opencv.imgproc.Imgproc;
import org.opencv.android.Utils;

import java.nio.DoubleBuffer;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import static java.lang.Math.abs;
import static java.lang.Math.pow;
import static org.opencv.core.CvType.*;

public class ImageProcessor {
    private Bitmap bitmap; // Bitmap con informacion de la imagen
    private Mat flooded; // Mat para ser inundado por el algoritmo
    private Mat img;

    private Bitmap pathBitmap;

    private Integer search_square_size; // tamaño del cuadrado de la región de busqueda cercana
    private Integer search_times; // cantidad de tanteos para buscar el cuadrado
    private Integer square_size; // tamaño del cuadrado de busqueda

    private Scalar lower, upper;
    private Mat confidence, shapeMask, grey_scale; // matriz de confianza
    private Mat sobel_x, sobel_y; // espacio para derivadas
    private List<Pair<Integer,Integer>> square; // cuadrado de busqueda
    private Random r;
    private ThreadProcess thread;
    private Long iterations;
    private UpdateImageListener updateImageListener;
    private Integer height, width;
    private Mat black;
    private FinishProcessListener finishListener;

    protected ImageProcessor(Context ctx){
        OpenCVLoader.initDebug();

        img = null;
        flooded = null;
        thread = new ThreadProcess(); // el algoritmo pesado se ejecuta en un thread
        iterations = 0l;
        finishListener = null;

        thread.setListener(new ThreadListener() {
            @Override
            public boolean runThread() {
                return runIteration();
            }
            public void threadFinish(){
                if (finishListener != null) {
                    finishListener.finish();
                }
            }
        });

        r = new Random();

        // el tamaño del cuadrado de busqueda se configura en un archivo
        search_square_size = ctx.getResources().getInteger(R.integer.search_square_size);
        // el numero de tanteos de cuadrados se configura en un archivo
        search_times = ctx.getResources().getInteger(R.integer.search_times);
        // el tamaño del cuadrado de busqueda se configura en un archivo
        square_size = ctx.getResources().getInteger(R.integer.square_size);

        lower = new Scalar(100);
        upper = new Scalar(150);

        height = ctx.getResources().getInteger(R.integer.height);
        width = ctx.getResources().getInteger(R.integer.width);


        black = new Mat(square_size, square_size, CV_8UC1, new Scalar(0));

    }
    public void setBitmap(Bitmap bitmap){
        // esta funcion configura que bitmap se utilizará para el procesamiento
        // también realiza cálculos iniciales muy necesarios

        if (img == null){
            img = new Mat();
        }

        this.bitmap = bitmap;
        Bitmap bmp32 = bitmap.copy(Bitmap.Config.ARGB_8888, true);

        Mat aux = new Mat();
        Utils.bitmapToMat(bmp32, aux);
        Size sz = new Size(this.width,this.height);
        Imgproc.resize(aux, img ,sz);

        // Matrices necesarias para el algoritmo
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

        Mat mask = new Mat();
        Mat inputMatSmall = new Mat();
        Mat inputMat = new Mat();
        Mat grayImage = new Mat();

        Bitmap bmp32 = pathBitmap.copy(Bitmap.Config.ARGB_8888, true);
        Utils.bitmapToMat(bmp32, inputMatSmall);

        Size sz = new Size(this.width,this.height);
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

        flooded.convertTo(confidence, 1, -1, 255);
    }
    public Bitmap getFloodedBitmap(){
        Bitmap outputBitmap = Bitmap.createBitmap(
                width,
                height,
                Bitmap.Config.ARGB_8888
        );

        Utils.matToBitmap(flooded, outputBitmap);
        return outputBitmap;
    }
    public void startAlgorithm(){
        Log.d("ImageEditLogs","Algorithm started");
        this.thread.start();
        /*for (int i = 0;i < 11;i++) {
            Log.d("ImageEditLogs","Running iteration "+i);
            runIteration();
        }*/
    }
    private boolean runIteration() {
        /// correr una iteración del algoritmo


        /// buscamos contornos

        List<MatOfPoint> points = new ArrayList<>();

        Core.inRange(flooded, lower, upper,shapeMask);

        Mat hierarchy = new Mat();
        Imgproc.findContours(flooded.clone(), points, hierarchy, Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
        hierarchy.release();

        /// Buscamos el mejor beneficio
        double best_benefit = Double.NEGATIVE_INFINITY;
        Pair<Integer,Integer> best_benefit_point = null;

        Imgproc.cvtColor(img, grey_scale, Imgproc.COLOR_BGR2GRAY);

        Imgproc.Sobel(grey_scale, sobel_y, 5, 1, 0);
        Imgproc.Sobel(grey_scale, sobel_x, 5, 0, 1);

        Core.multiply(sobel_x, new Scalar(-1), sobel_x);

        /****** PARTE 1 ******/

        for (MatOfPoint contorno : points){ // por cada contorno distinto

            // ## necesitamos generar las normales de cada punto del contorno
            List<Point> border_normal = new ArrayList<>(); // normales al borde
            Point []local_points = contorno.toArray();
            int n = local_points.length;

            for (int i = 0;i < n;i++){
                double dx = local_points[i].x - local_points[(i-1+n)%n].x;
                double dy = local_points[i].y - local_points[(i-1+n)%n].y;

                // # esta formula nos da la normal. no le damos importancia a la orientacion
                border_normal.add(new Point(dy, -dx));
            }

            int index = 0;

            for (Point border_point : local_points){
                int x = (int)border_point.x;
                int y = (int)border_point.y;

                // # consigo la confianza del punto del contorno actual
                double sum_confidence = 0;

                for (Pair<Integer,Integer> dd : square) {
                    int dy = dd.first;
                    int dx = dd.second;
                    double []v = shapeMask.get(y + dy, x + dx);

                    if (v[0] < 0.1f){ // problemas reportados con esta linea.
                        // fuera de la zona a retocar
                        sum_confidence += confidence.get(y + dy, x + dx)[0];
                    }
                }
                sum_confidence /= square.size();

                // consigo la componente normal del gradiente
                double nx = border_normal.get(index).x;
                double ny = border_normal.get(index).y;

                // # consigo el gradiente mas grande de la region
                double max_grad = 0d;
                Pair<Double,Double> max_grad_value = new Pair<>(0d,0d);

                for (Pair<Integer,Integer> dd : square){
                    int dy = dd.first;
                    int dx = dd.second;
                    double []v = shapeMask.get(y + dy, x + dx);

                    if (v[0] < 0.1f){
                        double vx = sobel_x.get(y, x)[0];
                        double vy = sobel_y.get(y, x)[0];

                        double p = vx * vx + vy * vy;

                        if (p > max_grad){
                            max_grad = p;
                            max_grad_value = new Pair<>(vx, vy);
                        }

                    }
                }

                // producto escalar del gradiente con la normal acorde a la formu
                double d = max_grad_value.first * nx + max_grad_value.second * ny;

                //el beneficio es la confianza por el factor d
                double benefit = abs(d * sum_confidence);

                // buscamos maximizar el beneficio
                if (benefit > best_benefit){
                    best_benefit = benefit;
                    best_benefit_point = new Pair<>(x, y);
                }

                index ++;
            }

        }

        if (best_benefit_point == null){
            Log.d("ImageEditLogs","Termino el algoritmo");
            this.finishListener.finish();
            return false; // significa que terminamos

        }

        /****** PARTE 2 ******/

        int px = best_benefit_point.first;
        int py = best_benefit_point.second;

        Pair<Integer, Integer> best_patch = new Pair<>(px, py);
        Double patch_distance = Double.POSITIVE_INFINITY;

        for (Integer i = 0;i < search_times;i++){
            double sigma = (double)search_square_size/32;
            double mu_x = (double)px;
            double mu_y = (double)py;

            int x = (int)(r.nextGaussian() * sigma + mu_x);
            int y = (int)(r.nextGaussian() * sigma + mu_y);

            double []v = shapeMask.get(y , x );

            if (v[0] > 254d){
                continue;
            }

            double total_sum = 0;

            for (int yi = -square_size/2;yi <= square_size/2;yi++){
                for (int xi = -square_size/2;xi <= square_size/2;xi++){
                    double sum = 0;
                    for (int cmp = 0;cmp < 3;cmp++){
                        int patch = (int)img.get(y + yi, x + xi)[cmp];
                        int original = (int)img.get(y + yi, x + xi)[cmp];

                        sum += (patch - original) * (patch - original);

                        total_sum += sum;
                    }
                }
            }

            if (total_sum < patch_distance){
                patch_distance = total_sum;
                best_patch = new Pair<>(x,y);
            }
        }

        int bx = best_patch.first;
        int by = best_patch.second;

        // ahora ejecutamos las copias
        //Log.d("ImageEditLogs","square size = " + square_size);
        Rect srcMat = new Rect(
                bx - square_size/2,
                by - square_size/2,
                square_size,
                square_size
                );
        Rect dstMat = new Rect(
                px - square_size/2,
                py - square_size/2,
                square_size,
                square_size
        );

        //Log.d("ImageEditLogs", srcMat.x + " " + srcMat.y + " -> " + dstMat.x + " " + dstMat.y);
        img.submat(srcMat).clone().copyTo( img.submat(dstMat) );
        confidence.submat(srcMat).clone().copyTo( confidence.submat(dstMat) );

        black.copyTo( flooded.submat(dstMat));
        //white.clone().copyTo( flooded.submat(dstMat) );

        if (iterations % 10 == 0){
            //Log.d("ImageEditLogs", "Actualizando imagen");
            Bitmap outputBitmap = Bitmap.createBitmap(
                    width,
                    height,
                    Bitmap.Config.ARGB_8888
            );

            Utils.matToBitmap(img, outputBitmap);

            this.updateImageListener.updateImage(
                    outputBitmap.copy(outputBitmap.getConfig(), false)
            );
        }
        iterations ++;

        return true;

    }

    public UpdateImageListener getUpdateImageListener() {
        return updateImageListener;
    }

    public void setUpdateImageListener(UpdateImageListener updateImageListener) {
        this.updateImageListener = updateImageListener;
    }

    public void cancel(){
        this.thread.finish();
    }

    public FinishProcessListener getFinishListener() {
        return finishListener;
    }

    public void setFinishListener(FinishProcessListener finishListener) {
        this.finishListener = finishListener;
    }
}
