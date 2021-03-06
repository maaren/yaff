// YAFF is yet another force-field code.
// Copyright (C) 2011 Toon Verstraelen <Toon.Verstraelen@UGent.be>,
// Louis Vanduyfhuys <Louis.Vanduyfhuys@UGent.be>, Center for Molecular Modeling
// (CMM), Ghent University, Ghent, Belgium; all rights reserved unless otherwise
// stated.
//
// This file is part of YAFF.
//
// YAFF is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// YAFF is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, see <http://www.gnu.org/licenses/>
//
// --


#ifndef YAFF_ICLIST_H
#define YAFF_ICLIST_H

#include "dlist.h"

typedef struct {
  long kind;       // Numerical code for the type of internal coordinate, e.g. bond, angle, ...
  long i0, sign0;  // row index and sign flip of relative vector 0 in ``DeltaList`` object
  long i1, sign1;  // row index and sign flip of relative vector 1 in ``DeltaList`` object
  long i2, sign2;  // row index and sign flip of relative vector 2 in ``DeltaList`` object
  long i3, sign3;  // row index and sign flip of relative vector 3 in ``DeltaList`` object
  double value;    // value of internal coordinate
  double grad;     // derivative of energy towards internal coordinate
} iclist_row_type;

void iclist_forward(dlist_row_type* deltas, iclist_row_type* ictab, long nic);
void iclist_back(dlist_row_type* deltas, iclist_row_type* ictab, long nic);

#endif
