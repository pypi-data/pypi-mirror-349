### Cython interface to Voro++  ###
# The code constitutes an extension to the project
# https://github.com/chr1shr/voro
# for performing 3D voronoi tesselations

### Voro++ copyright & acknowledgments ###
# Voro++ Copyright (c) 2008, The Regents of the University of California, 
# through Lawrence Berkeley National Laboratory. All rights reserved.

# The code so far interfaces only a part of features of Voro++
# For further development, see data structures of Voro++ 
# https://math.lbl.gov/voro++/doc/refman/annotated.html
# For bug reports, send an email to Siyu Chen <sc2090@cam.ac.uk>


from libcpp.vector cimport vector
from libcpp cimport bool as cbool
from cython.operator cimport dereference


cdef extern from 'voro++.hh' namespace 'voro':
    cdef cppclass container_base:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1container__base.html
        pass

    cdef cppclass container_periodic_base:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1container__periodic__base.html
        pass

    cdef cppclass container:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1container.html
        container(double, double, double, double, double, double, 
                  int, int, int, cbool, cbool, cbool, int) except +
        cbool compute_cell(voronoicell_neighbor &c, c_loop_all &vl)
        cbool point_inside(double, double, double)
        void put(int, double, double, double)

    cdef cppclass container_poly:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1container__poly.html
        container_poly(double, double, double, double, double, double, 
                       int, int, int, cbool, cbool, cbool, int) except +
        cbool compute_cell(voronoicell_neighbor &c, c_loop_all &vl)
        cbool point_inside(double, double, double)
        void put(int, double, double, double, double)

    cdef cppclass container_periodic:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1container__periodic.html
        container_periodic(double, double, double, double, double, double, 
                           int, int, int, int) except +
        cbool compute_cell(voronoicell_neighbor &c, c_loop_all_periodic &vl)
        void put(int, double, double, double)

    cdef cppclass container_periodic_poly:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1container__periodic__poly.html
        container_periodic_poly(double, double, double, double, double, double, 
                                int, int, int, int) except +
        cbool compute_cell(voronoicell_neighbor &c, c_loop_all_periodic &vl)
        void put(int, double, double, double, double)

    cdef cppclass voronoicell_neighbor:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1voronoicell__neighbor.html
        voronoicell()
        void centroid(double &cx, double &cy, double &cz)
        double volume()
        double max_radius_squared()
        double total_edge_distance()
        double surface_area()
        double number_of_faces()
        double number_of_edges()

        void vertex_orders(vector[int] &)
        void vertices(double, double, double, vector[double] &)
        void face_areas(vector[double] &)
        void face_orders(vector[int] &)
        void face_freq_table(vector[int] &)
        void face_vertices(vector[int] &)
        void face_perimeters(vector[double] &)
        void normals(vector[double] &)
        void neighbors(vector[int] &)

    cdef cppclass c_loop_all:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1c__loop__all.html
        c_loop_all(container_base &)
        cbool start()
        cbool inc()
        int pid()
        void pos(double &x, double &y, double &z)
        void pos(int &pid, double &x, double &y, double &z, double &r)

    cdef cppclass c_loop_all_periodic:
        # https://math.lbl.gov/voro++/doc/refman/classvoro_1_1c__loop__all__periodic.html
        c_loop_all_periodic(container_periodic_base &)
        cbool start()
        cbool inc()
        int pid()
        void pos(double &x, double &y, double &z)
        void pos(int &pid, double &x, double &y, double &z, double &r)


cdef class Cell:
    cdef voronoicell_neighbor *thisptr
    cdef int id
    cdef double x, y, z
    cdef double r

    def __cinit__(self):
        self.thisptr = new voronoicell_neighbor()

    def __dealloc__(self):
        del self.thisptr

    @property
    def pos(self):
        return (self.x, self.y, self.z)

    @property
    def radius(self):
        return self.r

    @property
    def id(self):
        return self.id

    def volume(self):
        return self.thisptr.volume()
    def max_radius_squared(self):
        return self.thisptr.max_radius_squared()
    def total_edge_distance(self):
        return self.thisptr.total_edge_distance()
    def surface_area(self):
        return self.thisptr.surface_area()
    def number_of_faces(self):
        return self.thisptr.number_of_faces()
    def number_of_edges(self):
        return self.thisptr.number_of_edges()

    def centroid(self):
            cdef double cx = 0
            cdef double cy = 0
            cdef double cz = 0
            self.thisptr.centroid(cx, cy, cz)
            x, y, z = self.pos
            return (cx + x, cy + y, cz + z)

    def vertex_orders(self):
        cdef vector[int] v
        self.thisptr.vertex_orders(v)
        return v

    def vertices(self):
        cdef vector[double] v
        self.thisptr.vertices(self.x, self.y, self.z, v)
        return list(zip(v[::3], v[1::3], v[2::3]))

    def face_areas(self):
        cdef vector[double] v
        self.thisptr.face_areas(v)
        return v

    def face_freq_table(self):
        cdef vector[int] v
        self.thisptr.face_freq_table(v)
        return v

    def face_vertices(self):
        cdef vector[int] v
        self.thisptr.face_vertices(v)

        faces = []
        it = iter(v)
    
        for n in it:
            face = [next(it) for _ in range(n)]
            faces.append(face)

        return faces

    def face_perimeters(self):
        cdef vector[double] v
        self.thisptr.face_perimeters(v)
        return v

    def normals(self):
        cdef vector[double] v
        self.thisptr.normals(v)
        return list(zip(v[::3], v[1::3], v[2::3]))

    def neighbors(self):
        # Note: Voro++ uses postive cell ids to refer to internal cells
        # while using negative cell ids to refer to boundary cells
        # e.g. v[3]=-6 means that the cell neighbors the boundary cell with id=6

        cdef vector[int] v
        self.thisptr.neighbors(v)
        return v

    def __str__(self):
        return '<Cell {0}>'.format(self.id)

    def __repr__(self):
        return '<Cell {0}>'.format(self.id)


cdef class Container:
    cdef container *thisptr
    def __cinit__(self, double ax_, double bx_, double ay_, double by_, double az_, double bz_, 
                  int nx_, int ny_, int nz_, cbool xperiodic_, cbool yperiodic_, cbool zperiodic_, 
                  int init_mem):
        self.thisptr = new container(ax_, bx_, ay_, by_, az_, bz_, nx_, ny_, nz_, 
                                     xperiodic_, yperiodic_, zperiodic_, init_mem)

    def __dealloc__(self):
        del self.thisptr

    def put(self, int n, double x, double y, double z):
        assert self.thisptr.point_inside(x, y, z)
        self.thisptr.put(n, x, y, z)


    def get_cells(self):
        cdef container_base *baseptr = (<container_base *>(self.thisptr))
        cdef c_loop_all *vl = new c_loop_all(dereference(baseptr))

        cells = []
        cell = Cell()

        if not vl.start():
            del vl
            raise ValueError('Failed to start loop')

        while True:
            if self.thisptr.compute_cell(dereference(cell.thisptr), dereference(vl)):
                cell.id = vl.pid()
                vl.pos(cell.x, cell.y, cell.z)
                cell.r = 0
                cells.append(cell)
                cell = Cell()
            if not vl.inc(): break
        del vl
        return cells
    

cdef class ContainerPoly:
    cdef container_poly *thisptr
    def __cinit__(self, double ax_, double bx_, double ay_, double by_, double az_, double bz_, 
                  int nx_, int ny_, int nz_, cbool xperiodic_, cbool yperiodic_, cbool zperiodic_, 
                  int init_mem):
        self.thisptr = new container_poly(ax_, bx_, ay_, by_, az_, bz_, nx_, ny_, nz_, 
                                          xperiodic_, yperiodic_, zperiodic_, init_mem)

    def __dealloc__(self):
        del self.thisptr

    def put(self, int n, double x, double y, double z, double r):
        assert self.thisptr.point_inside(x, y, z)
        self.thisptr.put(n, x, y, z, r)

    def get_cells(self):
        cdef container_base *baseptr = (<container_base *>(self.thisptr))
        cdef c_loop_all *vl = new c_loop_all(dereference(baseptr))

        if not vl.start():
            del vl
            raise ValueError('Failed to start loop')

        cells = []
        cell = Cell()
        while True:
            if self.thisptr.compute_cell(dereference(cell.thisptr), dereference(vl)):
                vl.pos(cell.id, cell.x, cell.y, cell.z, cell.r)
                cells.append(cell)
                cell = Cell()
            if not vl.inc(): break
        del vl
        return cells


cdef class ContainerPeriodic:
    cdef container_periodic *thisptr
    def __cinit__(self, double bx_, double bxy_, double by_, double bxz_, double byz_, double bz_, 
                  int nx_, int ny_, int nz_, int init_mem):
        self.thisptr = new container_periodic(bx_, bxy_, by_, bxz_, byz_, bz_, nx_, ny_, nz_, init_mem)

    def __dealloc__(self):
        del self.thisptr

    def put(self, int n, double x, double y, double z):
        self.thisptr.put(n, x, y, z)

    def get_cells(self):
        cdef container_periodic_base *baseptr = (<container_periodic_base *>(self.thisptr))
        cdef c_loop_all_periodic *vl = new c_loop_all_periodic(dereference(baseptr))

        cells = []
        cell = Cell()

        if not vl.start():
            del vl
            raise ValueError('Failed to start loop')

        while True:
            if self.thisptr.compute_cell(dereference(cell.thisptr), dereference(vl)):
                cell.id = vl.pid()
                vl.pos(cell.x, cell.y, cell.z)
                cell.r = 0
                cells.append(cell)
                cell = Cell()
            if not vl.inc(): break
        del vl
        return cells


cdef class ContainerPeriodicPoly:
    cdef container_periodic_poly *thisptr
    def __cinit__(self, double bx_, double bxy_, double by_, double bxz_, double byz_, double bz_, 
                  int nx_, int ny_, int nz_, int init_mem):
        self.thisptr = new container_periodic_poly(bx_, bxy_, by_, bxz_, byz_, bz_, nx_, ny_, nz_, init_mem)

    def __dealloc__(self):
        del self.thisptr

    def put(self, int n, double x, double y, double z, double r):
        self.thisptr.put(n, x, y, z, r)

    def get_cells(self):
        cdef container_periodic_base *baseptr = (<container_periodic_base *>(self.thisptr))
        cdef c_loop_all_periodic *vl = new c_loop_all_periodic(dereference(baseptr))

        if not vl.start():
            del vl
            raise ValueError('Failed to start loop')

        cells = []
        cell = Cell()
        while True:
            if self.thisptr.compute_cell(dereference(cell.thisptr), dereference(vl)):
                vl.pos(cell.id, cell.x, cell.y, cell.z, cell.r)
                cells.append(cell)
                cell = Cell()
            if not vl.inc(): break
        del vl
        return cells
