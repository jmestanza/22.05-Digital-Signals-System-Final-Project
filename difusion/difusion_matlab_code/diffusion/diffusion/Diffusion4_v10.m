function [Iout] = Diffusion4(I_in, varargin)
%function [Iout] = Diffusion4(I_in, varargin)
%
%Non linear diffusion with 4 neighbours.
%
%INPUT
%Iin			=		Input image.
%
%PARAMETERS
%see from the code
%
%OUTPUT
%Iout			=		Output image, after diffusion.
%
%If you use this code, please reference any/some of my papers (see http://atc.ugr.es/~jarnor)
%
%Author: Jarno Ralli
%E-mail: jarno@ralli.fi
%
%Copyright 2012, Jarno Ralli
%
%This program is free software: you can redistribute it and/or modify
%it under the terms of the GNU Lesser General Public License as published by
%the Free Software Foundation, either version 3 of the License, or
%(at your option) any later version.
%
%This program is distributed in the hope that it will be useful,
%but WITHOUT ANY WARRANTY; without even the implied warranty of
%MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%GNU Lesser General Public License for more details.
%
%You should have received a copy of the GNU Lesser General Public License
%along with this program.  If not, see <http://www.gnu.org/licenses/>.

param.alpha = 25;		%Smoothness
param.outer_iter = 5;		%Number of outer iterations (lagged diffusivity iterations)

param = setParameters(param, varargin{:});

Iout = single(I_in);
[rows cols dims]= size(Iout);

for iter=0:param.outer_iter

	%Calculate diffusion weights
	[wW wN wE wS] = DiffWeights(Iout); 

	a_ver = -param.alpha*wN;
	b_ver = 2 + param.alpha*(wN+wS);
	c_ver = -param.alpha*wS;

	a_hor = -param.alpha*wW';
	b_hor = 2 + param.alpha*(wW+wE)';
	c_hor = -param.alpha*wE';

	for k=1:dims
		ver = TDMA( a_ver, b_ver, c_ver, Iout(:,:,k) );
		hor = TDMA( a_hor, b_hor, c_hor, Iout(:,:,k)' )';
		Iout(:,:,k) = ver + hor;
	end
end

Iout = uint8(Iout);

%--------------------------------------------------------------------------------------------------------------
%--- TDMA
%--- Adaption from the code available at Wikipedia (http://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm)
%--------------------------------------------------------------------------------------------------------------
function x = TDMA(a,b,c,d)
%function x = TDMA(a,b,c,d)
	
	%a, b, c are the column vectors for the compressed tridiagonal matrix, d is the right vector
	[rows cols dims]= size(a); % n is the number of rows

	%Modify the first-row coefficients
	c(1,:) = c(1,:) ./ b(1,:);	% Division by zero risk.
	d(1,:) = d(1,:) ./ b(1,:);	% Division by zero would imply a singular matrix.

	for i = 2:rows-1
		temp = 1./( b(i,:) - a(i,:) .* c(i-1,:) );
		c(i,:) = c(i,:) .* temp;
		d(i,:) = (d(i,:) - a(i,:) .* d(i-1,:)) .* temp;
	end
	
	d(rows,:) = ( d(rows,:) - a(rows,:) .* d(rows-1,:) )./( b(rows,:) - a(rows,:) .* c(rows-1,:) );
	
	%Now back substitute.
	x(rows,:) = d(rows,:);
	for i = rows-1:-1:1
		x(i,:) = d(i,:) - c(i,:) .* x(i + 1,:);
	end

%----------------------
%--- DiffWeights
%----------------------
function [wW wN wE wS] = DiffWeights(D)
%function [wW wN wE wS] = DiffWeights(D)
%
%Calculates diffusion weights using `Brox 6-point scheme'.

	  [rows cols frames] = size( D );

	  %Spatial differences
	  Dver = imfilter(D,[0.25 0 -0.25]','replicate');
	  Dhor = imfilter(D,[0.25 0 -0.25],'replicate');
	  
	  wW = (circshift(D,[0 1 0])-D).^2 + (Dver+circshift(Dver,[0 1 0])).^2;
	  wE = (circshift(D,[0 -1 0])-D).^2 + (Dver+circshift(Dver,[0 -1 0])).^2;
	  wN = (circshift(D,[1 0 0])-D).^2 + (Dhor+circshift(Dhor,[1 0 0])).^2;
	  wS = (circshift(D,[-1 0 0])-D).^2 + (Dhor+circshift(Dhor,[-1 0 0])).^2;
	  
	  %Find the maximum derivative
	  wW = max(wW,[],3);
	  wE = max(wE,[],3);
	  wN = max(wN,[],3);
	  wS = max(wS,[],3);
  
	  wW = 1./realsqrt( wW + 0.00001 );
	  wE = 1./realsqrt( wE + 0.00001 );
	  wN = 1./realsqrt( wN + 0.00001 );
	  wS = 1./realsqrt( wS + 0.00001 );
	  
	  wW(:,1,:) = 0;
	  wE(:,end,:) = 0;
	  wN(1,:,:) = 0;
	  wS(end,:,:) = 0;

%----------------------
%--- setParameters
%----------------------
function new_struct = setParameters(old_struct,varargin)
%function new_param = setParameters(old_param,varargin)
%
%Changes parameters in a parameter struct. The new parameters are given as
%['name',value] corresponding pairs in the varargin.
%
%INPUT
%old_struct     =       Old structure
%varargin       =       ['name',value]
%OUTPUT
%new_struct     =       New structure
%
	n_param = length(varargin);
	new_struct = old_struct;

	for i=1:2:n_param

		%Extract parameter name
		p_name = varargin{i};

		%If for the parameter (name) exists a value...
		if i+1<=n_param
			%then extract the value
			p_value = varargin{i+1};
			
			%and if the p_name exists in the structure
			if isfield(new_struct, p_name)
				%set its value
				new_struct=setfield(new_struct, p_name, p_value);
			else
				%error(['setParameters error: unkown parameter name "',p_name,'". ',num2str(i)]);
			end
		end

	end