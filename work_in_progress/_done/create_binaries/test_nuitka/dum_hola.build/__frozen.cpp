// This provides the frozen (compiled bytecode) files that are included if
// any.
#include <Python.h>

// Blob from which modules are unstreamed.
#if defined(_WIN32) && defined(_NUITKA_EXE)
extern const unsigned char* constant_bin;
#else
extern "C" const unsigned char constant_bin[];
#endif

#define stream_data constant_bin

// These modules should be loaded as bytecode. They may e.g. have to be loadable
// during "Py_Initialize" already, or for irrelevance, they are only included
// in this un-optimized form. These are not compiled by Nuitka, and therefore
// are not accelerated at all, merely bundled with the binary or module, so
// that CPython library can start out finding them.

void copyFrozenModulesTo( void* destination )
{
    _frozen frozen_modules[] = {
        { (char *)"_bootlocale", (unsigned char *)&constant_bin[ 7004097 ], 1085 },
        { (char *)"_collections_abc", (unsigned char *)&constant_bin[ 7005182 ], 29678 },
        { (char *)"_compat_pickle", (unsigned char *)&constant_bin[ 7034860 ], 7848 },
        { (char *)"_weakrefset", (unsigned char *)&constant_bin[ 7042708 ], 8462 },
        { (char *)"abc", (unsigned char *)&constant_bin[ 7051170 ], 7906 },
        { (char *)"ast", (unsigned char *)&constant_bin[ 7059076 ], 12346 },
        { (char *)"codecs", (unsigned char *)&constant_bin[ 7071422 ], 35344 },
        { (char *)"collections", (unsigned char *)&constant_bin[ 7106766 ], -47872 },
        { (char *)"collections.abc", (unsigned char *)&constant_bin[ 7005182 ], 29678 },
        { (char *)"copyreg", (unsigned char *)&constant_bin[ 7154638 ], 4606 },
        { (char *)"dis", (unsigned char *)&constant_bin[ 7159244 ], 14686 },
        { (char *)"encodings", (unsigned char *)&constant_bin[ 7173930 ], -3890 },
        { (char *)"encodings.aliases", (unsigned char *)&constant_bin[ 7177820 ], 7606 },
        { (char *)"encodings.ascii", (unsigned char *)&constant_bin[ 7185426 ], 2050 },
        { (char *)"encodings.cp437", (unsigned char *)&constant_bin[ 7187476 ], 7425 },
        { (char *)"encodings.idna", (unsigned char *)&constant_bin[ 7194901 ], 6500 },
        { (char *)"encodings.latin_1", (unsigned char *)&constant_bin[ 7201401 ], 2062 },
        { (char *)"encodings.utf_8", (unsigned char *)&constant_bin[ 7203463 ], 1750 },
        { (char *)"enum", (unsigned char *)&constant_bin[ 7205213 ], 16495 },
        { (char *)"functools", (unsigned char *)&constant_bin[ 7221708 ], 23663 },
        { (char *)"genericpath", (unsigned char *)&constant_bin[ 7245371 ], 3973 },
        { (char *)"heapq", (unsigned char *)&constant_bin[ 7249344 ], 15084 },
        { (char *)"importlib", (unsigned char *)&constant_bin[ 7264428 ], -3941 },
        { (char *)"importlib._bootstrap", (unsigned char *)&constant_bin[ 7268369 ], 31839 },
        { (char *)"importlib._bootstrap_external", (unsigned char *)&constant_bin[ 7300208 ], 41586 },
        { (char *)"importlib.machinery", (unsigned char *)&constant_bin[ 7341794 ], 1064 },
        { (char *)"inspect", (unsigned char *)&constant_bin[ 7342858 ], 84334 },
        { (char *)"io", (unsigned char *)&constant_bin[ 7427192 ], 3499 },
        { (char *)"keyword", (unsigned char *)&constant_bin[ 7430691 ], 1981 },
        { (char *)"linecache", (unsigned char *)&constant_bin[ 7432672 ], 4118 },
        { (char *)"locale", (unsigned char *)&constant_bin[ 7436790 ], 36606 },
        { (char *)"opcode", (unsigned char *)&constant_bin[ 7473396 ], 5741 },
        { (char *)"operator", (unsigned char *)&constant_bin[ 7479137 ], 14848 },
        { (char *)"os", (unsigned char *)&constant_bin[ 7493985 ], 29903 },
        { (char *)"pickle", (unsigned char *)&constant_bin[ 7523888 ], 46849 },
        { (char *)"posixpath", (unsigned char *)&constant_bin[ 7570737 ], 11176 },
        { (char *)"re", (unsigned char *)&constant_bin[ 7581913 ], 14493 },
        { (char *)"reprlib", (unsigned char *)&constant_bin[ 7596406 ], 5970 },
        { (char *)"sre_compile", (unsigned char *)&constant_bin[ 7602376 ], 10961 },
        { (char *)"sre_constants", (unsigned char *)&constant_bin[ 7613337 ], 5982 },
        { (char *)"sre_parse", (unsigned char *)&constant_bin[ 7619319 ], 22376 },
        { (char *)"stat", (unsigned char *)&constant_bin[ 7641695 ], 4203 },
        { (char *)"stringprep", (unsigned char *)&constant_bin[ 7645898 ], 13024 },
        { (char *)"struct", (unsigned char *)&constant_bin[ 7658922 ], 388 },
        { (char *)"token", (unsigned char *)&constant_bin[ 7659310 ], 3714 },
        { (char *)"tokenize", (unsigned char *)&constant_bin[ 7663024 ], 20507 },
        { (char *)"types", (unsigned char *)&constant_bin[ 7683531 ], 8781 },
        { (char *)"warnings", (unsigned char *)&constant_bin[ 7692312 ], 12978 },
        { (char *)"weakref", (unsigned char *)&constant_bin[ 7705290 ], 20290 },
        { NULL, NULL, 0 }
    };

    memcpy(
        destination,
        frozen_modules,
        ( _NUITKA_FROZEN + 1 ) * sizeof( struct _frozen )
    );
}
