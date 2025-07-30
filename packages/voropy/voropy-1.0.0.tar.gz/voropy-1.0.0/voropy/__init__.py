from voropy.voroplusplus import (
    Container as _Container,
    ContainerPoly as _ContainerPoly,
    ContainerPeriodic as _ContainerPeriodic,
    ContainerPeriodicPoly as _ContainerPeriodicPoly,
)


class Container(list):
    def __init__(self, points, dimensions, origin=[0,0,0], periodic=False, radii=None, blocks=None):

        ax, ay, az = origin[0], origin[1], origin[2]
        bx, by, bz = dimensions[0], dimensions[1], dimensions[2]

        try:
            xperiodic, yperiodic, zperiodic = periodic
        except TypeError:
            xperiodic = yperiodic = zperiodic = periodic

        Lx, Ly, Lz = bx - ax, by - ay, bz - az

        N = len(points)

        # Make underlying computational grid
        if blocks is None:
            V = Lx * Ly * Lz
            Nthird = (N/V)**(1/3)
            blocks = round(Nthird * Lx), round(Nthird * Ly), round(Nthird * Lz)

        try:
            nx, ny, nz = blocks
        except TypeError:
            nx = ny = nz = blocks
        nx = max(int(nx), 1)
        ny = max(int(ny), 1)
        nz = max(int(nz), 1)
        self.blocks = nx, ny, nz

        def modulo(n, lmin, l, periodic):
            if periodic:
                v = (float(n) - lmin) % l + lmin
                return v
            else:
                return float(n)

        if radii is not None:
            assert len(radii) == len(points)
            self._container = _ContainerPoly(ax, bx, 
                                             ay, by, 
                                             az, bz, 
                                             nx, ny, nz, 
                                             xperiodic, yperiodic, zperiodic, 
                                             len(points))

            for n, (x, y, z), r in zip(range(len(points)), points, radii):
                try:
                    rx, ry, rz = (modulo(x, ax, Lx, xperiodic),
                                  modulo(y, ay, Ly, yperiodic),
                                  modulo(z, az, Lz, zperiodic))
                    self._container.put(n, rx, ry, rz, r)
                except AssertionError:
                    raise ValueError(f'Could not insert point {n} at ({rx}, {ry}, {rz}): point not inside the box.')
        else:
            self._container = _Container(
                ax, bx, 
                ay, by, 
                az, bz, 
                nx, ny, nz, 
                xperiodic, yperiodic, zperiodic, 
                len(points)
            )

            for n, (x, y, z) in enumerate(points):
                rx, ry, rz = (modulo(x, ax, Lx, xperiodic), 
                              modulo(y, ay, Ly, yperiodic), 
                              modulo(z, az, Lz, zperiodic))
                try:
                    self._container.put(n, rx, ry, rz)
                except AssertionError:
                    raise ValueError(f'Could not insert point {n} at ({rx}, {ry}, {rz}): point not inside the box.')

        cells = self._container.get_cells()
        list.__init__(self, cells)

        if len(self) != len(points):
            error_message = (
                f'{len(self)} voronoi cells for {len(points)} points\n'
                'Possible reasons and solutions:\n'
                '(1) Points on the non-periodic boundary -> move the points into the box\n'
                '(2) Overlapping points -> jitter the points or remove the duplicates\n'
                'If this error persists, please report it to Siyu Chen <sc2090@cam.ac.uk>'
                )
            raise ValueError(error_message)


class ContainerPeriodic(list):
    def __init__(self, points, lattice, radii=None, blocks=None):
        
        bx, by, bz = lattice[0][0], lattice[1][1], lattice[2][2]
        bxy, bxz, byz = lattice[1][0], lattice[2][0], lattice[2][1]

        Lx, Ly, Lz = bx, (by**2 + bxy**2)**(1/2), (bz**2 + bxz**2 + byz**2)**(1/2)

        N = len(points)

        # Make underlying computational grid
        if blocks is None:
            V = bx * by * bz
            Nthird = (N/V)**(1/3)
            blocks = round(Nthird * Lx), round(Nthird * Ly), round(Nthird * Lz)

        try:
            nx, ny, nz = blocks
        except TypeError:
            nx = ny = nz = blocks
        nx = max(int(nx), 1)
        ny = max(int(ny), 1)
        nz = max(int(nz), 1)
        self.blocks = nx, ny, nz

        if radii is not None:
            assert len(radii) == len(points)
            self._container = _ContainerPeriodicPoly(bx, 
                                                     bxy, by, 
                                                     bxz, byz, bz, 
                                                     nx, ny, nz, 
                                                     len(points))

            for n, (x, y, z), r in zip(range(len(points)), points, radii):
                self._container.put(n, x, y, z, r)
        else:
            self._container = _ContainerPeriodic(bx, 
                                                 bxy, by, 
                                                 bxz, byz, bz, 
                                                 nx, ny, nz, 
                                                 len(points))

            for n, (x, y, z) in enumerate(points):
                self._container.put(n, x, y, z)
        cells = self._container.get_cells()
        list.__init__(self, cells)
