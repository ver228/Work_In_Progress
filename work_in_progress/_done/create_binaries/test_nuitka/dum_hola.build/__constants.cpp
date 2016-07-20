
#include "nuitka/prelude.hpp"

// Sentinel PyObject to be used for all our call iterator endings. It will
// become a PyCObject pointing to NULL. It's address is unique, and that's
// enough for us to use it as sentinel value.
PyObject *_sentinel_value = NULL;

PyObject *const_int_0;
PyObject *const_int_pos_1;
PyObject *const_str_empty;
PyObject *const_dict_empty;
PyObject *const_bytes_empty;
PyObject *const_tuple_empty;
PyObject *const_str_plain_os;
PyObject *const_str_plain_end;
PyObject *const_str_plain_int;
PyObject *const_str_plain_len;
PyObject *const_str_plain_file;
PyObject *const_str_plain_iter;
PyObject *const_str_plain_open;
PyObject *const_str_plain_repr;
PyObject *const_str_plain_send;
PyObject *const_str_plain_site;
PyObject *const_str_plain_type;
PyObject *const_str_plain_PyQt4;
PyObject *const_str_plain_close;
PyObject *const_str_plain_print;
PyObject *const_str_plain_range;
PyObject *const_str_plain_throw;
PyObject *const_str_plain_types;
PyObject *const_str_plain___all__;
PyObject *const_str_plain___cmp__;
PyObject *const_str_plain___doc__;
PyObject *const_str_plain_compile;
PyObject *const_str_plain_dirname;
PyObject *const_str_plain_inspect;
PyObject *const_str_plain___dict__;
PyObject *const_str_plain___exit__;
PyObject *const_str_plain___file__;
PyObject *const_str_plain___iter__;
PyObject *const_str_plain___main__;
PyObject *const_str_plain___name__;
PyObject *const_str_plain___path__;
PyObject *const_str_plain___class__;
PyObject *const_str_plain___enter__;
PyObject *const_str_plain___cached__;
PyObject *const_str_plain___import__;
PyObject *const_str_plain___loader__;
PyObject *const_str_plain___module__;
PyObject *const_str_plain___package__;
PyObject *const_str_plain___builtins__;
PyObject *const_str_plain___metaclass__;

#if defined(_WIN32) && defined(_NUITKA_EXE)
#include <Windows.h>
const unsigned char* constant_bin;
struct __initResourceConstants
{
    __initResourceConstants()
    {
        constant_bin = (const unsigned char*)LockResource(
            LoadResource(
                NULL,
                FindResource(NULL, MAKEINTRESOURCE(3), RT_RCDATA)
            )
        );
    }
} __initResourceConstants_static_initializer;
#else
extern "C" const unsigned char constant_bin[];
#endif

static void _createGlobalConstants( void )
{
    NUITKA_MAY_BE_UNUSED PyObject *exception_type, *exception_value;
    NUITKA_MAY_BE_UNUSED PyTracebackObject *exception_tb;

#ifdef _MSC_VER
    // Prevent unused warnings in case of simple programs, the attribute
    // NUITKA_MAY_BE_UNUSED doesn't work for MSVC.
    (void *)exception_type; (void *)exception_value; (void *)exception_tb;
#endif

    const_int_0 = PyLong_FromUnsignedLong( 0ul );
    const_int_pos_1 = PyLong_FromUnsignedLong( 1ul );
    const_str_empty = UNSTREAM_STRING( &constant_bin[ 0 ], 0, 0 );
    const_dict_empty = _PyDict_NewPresized( 0 );
    assert( PyDict_Size( const_dict_empty ) == 0 );
    const_bytes_empty = UNSTREAM_BYTES( &constant_bin[ 0 ], 0 );
    const_tuple_empty = PyTuple_New( 0 );
    const_str_plain_os = UNSTREAM_STRING( &constant_bin[ 47 ], 2, 1 );
    const_str_plain_end = UNSTREAM_STRING( &constant_bin[ 262 ], 3, 1 );
    const_str_plain_int = UNSTREAM_STRING( &constant_bin[ 265 ], 3, 1 );
    const_str_plain_len = UNSTREAM_STRING( &constant_bin[ 268 ], 3, 1 );
    const_str_plain_file = UNSTREAM_STRING( &constant_bin[ 271 ], 4, 1 );
    const_str_plain_iter = UNSTREAM_STRING( &constant_bin[ 275 ], 4, 1 );
    const_str_plain_open = UNSTREAM_STRING( &constant_bin[ 279 ], 4, 1 );
    const_str_plain_repr = UNSTREAM_STRING( &constant_bin[ 283 ], 4, 1 );
    const_str_plain_send = UNSTREAM_STRING( &constant_bin[ 287 ], 4, 1 );
    const_str_plain_site = UNSTREAM_STRING( &constant_bin[ 291 ], 4, 1 );
    const_str_plain_type = UNSTREAM_STRING( &constant_bin[ 295 ], 4, 1 );
    const_str_plain_PyQt4 = UNSTREAM_STRING( &constant_bin[ 0 ], 5, 1 );
    const_str_plain_close = UNSTREAM_STRING( &constant_bin[ 299 ], 5, 1 );
    const_str_plain_print = UNSTREAM_STRING( &constant_bin[ 304 ], 5, 1 );
    const_str_plain_range = UNSTREAM_STRING( &constant_bin[ 309 ], 5, 1 );
    const_str_plain_throw = UNSTREAM_STRING( &constant_bin[ 314 ], 5, 1 );
    const_str_plain_types = UNSTREAM_STRING( &constant_bin[ 319 ], 5, 1 );
    const_str_plain___all__ = UNSTREAM_STRING( &constant_bin[ 324 ], 7, 1 );
    const_str_plain___cmp__ = UNSTREAM_STRING( &constant_bin[ 331 ], 7, 1 );
    const_str_plain___doc__ = UNSTREAM_STRING( &constant_bin[ 338 ], 7, 1 );
    const_str_plain_compile = UNSTREAM_STRING( &constant_bin[ 345 ], 7, 1 );
    const_str_plain_dirname = UNSTREAM_STRING( &constant_bin[ 352 ], 7, 1 );
    const_str_plain_inspect = UNSTREAM_STRING( &constant_bin[ 359 ], 7, 1 );
    const_str_plain___dict__ = UNSTREAM_STRING( &constant_bin[ 366 ], 8, 1 );
    const_str_plain___exit__ = UNSTREAM_STRING( &constant_bin[ 374 ], 8, 1 );
    const_str_plain___file__ = UNSTREAM_STRING( &constant_bin[ 382 ], 8, 1 );
    const_str_plain___iter__ = UNSTREAM_STRING( &constant_bin[ 390 ], 8, 1 );
    const_str_plain___main__ = UNSTREAM_STRING( &constant_bin[ 398 ], 8, 1 );
    const_str_plain___name__ = UNSTREAM_STRING( &constant_bin[ 406 ], 8, 1 );
    const_str_plain___path__ = UNSTREAM_STRING( &constant_bin[ 414 ], 8, 1 );
    const_str_plain___class__ = UNSTREAM_STRING( &constant_bin[ 422 ], 9, 1 );
    const_str_plain___enter__ = UNSTREAM_STRING( &constant_bin[ 431 ], 9, 1 );
    const_str_plain___cached__ = UNSTREAM_STRING( &constant_bin[ 440 ], 10, 1 );
    const_str_plain___import__ = UNSTREAM_STRING( &constant_bin[ 450 ], 10, 1 );
    const_str_plain___loader__ = UNSTREAM_STRING( &constant_bin[ 460 ], 10, 1 );
    const_str_plain___module__ = UNSTREAM_STRING( &constant_bin[ 470 ], 10, 1 );
    const_str_plain___package__ = UNSTREAM_STRING( &constant_bin[ 480 ], 11, 1 );
    const_str_plain___builtins__ = UNSTREAM_STRING( &constant_bin[ 491 ], 12, 1 );
    const_str_plain___metaclass__ = UNSTREAM_STRING( &constant_bin[ 503 ], 13, 1 );
}

// In debug mode we can check that the constants were not tampered with in any
// given moment. We typically do it at program exit, but we can add extra calls
// for sanity.
#ifndef __NUITKA_NO_ASSERT__
void checkGlobalConstants( void )
{

}
#endif


void createGlobalConstants( void )
{
    if ( _sentinel_value == NULL )
    {
#if PYTHON_VERSION < 300
        _sentinel_value = PyCObject_FromVoidPtr( NULL, NULL );
#else
        // The NULL value is not allowed for a capsule, so use something else.
        _sentinel_value = PyCapsule_New( (void *)27, "sentinel", NULL );
#endif
        assert( _sentinel_value );

        _createGlobalConstants();
    }
}
