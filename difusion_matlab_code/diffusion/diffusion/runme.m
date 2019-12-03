%Tested in Kubuntu 10.04.3 with gcc (Ubuntu 4.3.4-10ubuntu1) 4.3.4
%

%Read the images
disp('Reading images...')
I_l0 = imread('./images/DRIVSCO_left_0450.png');

%Apply diffusion
I_l0_diff = Diffusion4_v10( I_l0 );

figure, imagesc( uint8(I_l0) ), axis off, title('Original image')
figure, imagesc( uint8(I_l0_diff) ), axis off, title('Diffused image')
