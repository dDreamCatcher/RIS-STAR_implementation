function code = goldcode(n)
% Gold code/sequence generator
%
%     Usage
%         code = goldcode(n)
%
%     Input
%         n: one of 5, 6, 7, 9, 10, 11
%
%     Output
%         code: (N+2)xN matrix, where N = 2 ^ n - 1
%               Each row represents each gold sequence
%
% Reference: https://kr.mathworks.com/help/comm/ref/goldsequencegenerator.html

  if nargin < 1
    usage();
  end

  [p1, p2] = get_poly_order(n);
  P1 = poly_order_to_binary(p1, n);
  P2 = poly_order_to_binary(p2, n);

  N = 2 ^ n - 1;

  code = zeros(N + 2, N);
  code(1, :) = get_initial_sequence(P1, n, N);
  code(2, :) = get_initial_sequence(P2, n, N);
  for ii = 1:N
    code(ii + 2, :) = xor(code(1, :), [code(2, ii:end) code(2, 1:(ii - 1))]);
  end
  code(code == 0) = -1;

end

function [p1, p2] = get_poly_order(n)

  switch n
    case 5
      p1 = [5 2 0];
      p2 = [5 4 3 2 0];
    case 6
      p1 = [6 1 0];
      p2 = [6 5 2 1 0];
    case 7
      p1 = [7 3 0];
      p2 = [7 3 2 1 0];
    case 9
      p1 = [9 4 0];
      p2 = [9 6 4 3 0];
    case 10
      p1 = [10 3 0];
      p2 = [10 8 3 2 0];
    case 11
      p1 = [11 2 0];
      p2 = [11 8 5 2 0];
    otherwise
      usage();
  end
  % MATLAB and GNU Octave are 1-indexed
  p1 = p1 + 1;
  p2 = p2 + 1;

end

function P = poly_order_to_binary(p, n)
      
  P = 0;
  for pos = p
    P = bitset(P, pos);
  end
  P = de2bi(P, n + 1); % LSB on the left, MSB on the right

end

function sequence = get_initial_sequence(P, n, N)

  in = zeros(1, n);
  in(1) = 1;
  sequence = zeros(1, N);
  for jj = 1:N
    sequence(jj) = in(1);
    msb = mod(sum(in & P(1:(end - 1))), 2);
    in = [in(2:end) msb];
  end

end

function usage()

  error('n must be one of 5, 6, 7, 9, 10, or 11');

end