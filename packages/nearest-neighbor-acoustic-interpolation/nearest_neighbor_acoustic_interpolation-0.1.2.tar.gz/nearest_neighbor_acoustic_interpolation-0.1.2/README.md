# Nearest Neighbor Bi-linear Acoustic Interpolation

This code based was used for the development of near-field acoustic level maps associated with the paper: Mobley, Frank S., Alan T. Wall, and Stephen C. Campbell. "Translating jet noise measurements to near-field level maps with nearest neighbor bilinear smoothing interpolation." The Journal of the Acoustical Society of America 150.2 (2021): 687-693.

This code applies an image interpolation to a sparse matrix of acoustic levels. Then interpolates the dense matrix interatively to reduce the blockiness of the level maps. Each iteration, the known values from the sparse matrix are replaced to ensure that the values are not smoothed away.

This work was completed in association with research conducted at Wright-Patteron Air Force Base while employed at the 711 Human Performance Wing. It was cleared for public release with the public affairs clearance number AFRL-2025-2605 on 21 May 2025.