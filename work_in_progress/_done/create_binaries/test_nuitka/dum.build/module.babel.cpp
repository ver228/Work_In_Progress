// Generated code for Python source for module 'babel'
// created by Nuitka version 0.5.20

// This code is in part copyright 2016 Kay Hayen.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "nuitka/prelude.hpp"

#include "__helpers.hpp"

// The _module_babel is a Python object pointer of module type.

// Note: For full compatibility with CPython, every module variable access
// needs to go through it except for cases where the module cannot possibly
// have changed in the mean time.

PyObject *module_babel;
PyDictObject *moduledict_babel;

// The module constants used
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain_get_locale_identifier;
extern PyObject *const_str_plain_default_locale;
extern PyObject *const_str_plain___file__;
extern PyObject *const_str_plain_negotiate_locale;
static PyObject *const_str_digest_539b55806ce926f35e1b4324520ef591;
extern PyObject *const_str_plain___version__;
extern PyObject *const_str_plain___cached__;
static PyObject *const_str_digest_924d7d0f35b3d6fb8647d1e8cf9dd711;
extern PyObject *const_int_0;
extern PyObject *const_str_digest_34fba4047b17e32647652cd9e29451c9;
extern PyObject *const_str_plain_Locale;
extern PyObject *const_str_plain___path__;
extern PyObject *const_tuple_empty;
extern PyObject *const_str_plain_parse_locale;
extern PyObject *const_str_plain___loader__;
static PyObject *const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple;
extern PyObject *const_str_plain_dirname;
extern PyObject *const_str_plain_babel;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_digest_e248bf675f752bbffffa3cb66fd59b1a;
extern PyObject *const_str_plain_UnknownLocaleError;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_str_digest_539b55806ce926f35e1b4324520ef591 = UNSTREAM_STRING( &constant_bin[ 926145 ], 526, 0 );
    const_str_digest_924d7d0f35b3d6fb8647d1e8cf9dd711 = UNSTREAM_STRING( &constant_bin[ 926671 ], 17, 0 );
    const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple = PyTuple_New( 6 );
    PyTuple_SET_ITEM( const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, 0, const_str_plain_UnknownLocaleError ); Py_INCREF( const_str_plain_UnknownLocaleError );
    PyTuple_SET_ITEM( const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, 1, const_str_plain_Locale ); Py_INCREF( const_str_plain_Locale );
    PyTuple_SET_ITEM( const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, 2, const_str_plain_default_locale ); Py_INCREF( const_str_plain_default_locale );
    PyTuple_SET_ITEM( const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, 3, const_str_plain_negotiate_locale ); Py_INCREF( const_str_plain_negotiate_locale );
    PyTuple_SET_ITEM( const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, 4, const_str_plain_parse_locale ); Py_INCREF( const_str_plain_parse_locale );
    PyTuple_SET_ITEM( const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, 5, const_str_plain_get_locale_identifier ); Py_INCREF( const_str_plain_get_locale_identifier );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_babel( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_deefa2ace9ef29b89b1b29eecf0a7474;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_924d7d0f35b3d6fb8647d1e8cf9dd711 );
    codeobj_deefa2ace9ef29b89b1b29eecf0a7474 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_babel, 1, const_tuple_empty, 0, 0, CO_NOFREE );
}

// The module function declarations.


// The module function definitions.



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_babel =
{
    PyModuleDef_HEAD_INIT,
    "babel",   /* m_name */
    NULL,                /* m_doc */
    -1,                  /* m_size */
    NULL,                /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#endif

#if PYTHON_VERSION >= 300
extern PyObject *metapath_based_loader;
#endif

// The exported interface to CPython. On import of the module, this function
// gets called. It has to have an exact function name, in cases it's a shared
// library export. This is hidden behind the MOD_INIT_DECL.

MOD_INIT_DECL( babel )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_babel );
    }
    else
    {
        _init_done = true;
    }
#endif

#ifdef _NUITKA_MODULE
    // In case of a stand alone extension module, need to call initialization
    // the init here because that's the first and only time we are going to get
    // called here.

    // Initialize the constant values used.
    _initBuiltinModule();
    createGlobalConstants();

    // Initialize the compiled types of Nuitka.
    PyType_Ready( &Nuitka_Generator_Type );
    PyType_Ready( &Nuitka_Function_Type );
    PyType_Ready( &Nuitka_Method_Type );
    PyType_Ready( &Nuitka_Frame_Type );
#if PYTHON_VERSION >= 350
    PyType_Ready( &Nuitka_Coroutine_Type );
    PyType_Ready( &Nuitka_CoroutineWrapper_Type );
#endif

#if PYTHON_VERSION < 300
    _initSlotCompare();
#endif
#if PYTHON_VERSION >= 270
    _initSlotIternext();
#endif

    patchBuiltinModule();
    patchTypeComparison();

    // Enable meta path based loader if not already done.
    setupMetaPathBasedLoader();

#if PYTHON_VERSION >= 300
    patchInspectModule();
#endif

#endif

    createModuleConstants();
    createModuleCodeObjects();

    // puts( "in initbabel" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_babel = Py_InitModule4(
        "babel",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_babel = PyModule_Create( &mdef_babel );
#endif

    moduledict_babel = (PyDictObject *)((PyModuleObject *)module_babel)->md_dict;

    CHECK_OBJECT( module_babel );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_plain_babel, module_babel );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    PyObject *module_dict = PyModule_GetDict( module_babel );

    if ( PyDict_GetItem( module_dict, const_str_plain___builtins__ ) == NULL )
    {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then.
#if !defined(_NUITKA_EXE) || !0
        value = PyModule_GetDict( value );
#endif

#ifndef __NUITKA_NO_ASSERT__
        int res =
#endif
            PyDict_SetItem( module_dict, const_str_plain___builtins__, value );

        assert( res == 0 );
    }

#if PYTHON_VERSION >= 330
    PyDict_SetItem( module_dict, const_str_plain___loader__, metapath_based_loader );
#endif

    // Temp variables if any
    PyObject *exception_type = NULL, *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = -1;
    PyObject *tmp_args_element_name_1;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_assign_source_2;
    PyObject *tmp_assign_source_3;
    PyObject *tmp_assign_source_4;
    PyObject *tmp_assign_source_5;
    PyObject *tmp_assign_source_6;
    PyObject *tmp_assign_source_7;
    PyObject *tmp_assign_source_8;
    PyObject *tmp_assign_source_9;
    PyObject *tmp_assign_source_10;
    PyObject *tmp_assign_source_11;
    PyObject *tmp_assign_source_12;
    PyObject *tmp_called_name_1;
    PyObject *tmp_import_globals_1;
    PyObject *tmp_import_globals_2;
    PyObject *tmp_import_globals_3;
    PyObject *tmp_import_globals_4;
    PyObject *tmp_import_globals_5;
    PyObject *tmp_import_globals_6;
    PyObject *tmp_import_name_from_1;
    PyObject *tmp_import_name_from_2;
    PyObject *tmp_import_name_from_3;
    PyObject *tmp_import_name_from_4;
    PyObject *tmp_import_name_from_5;
    PyObject *tmp_import_name_from_6;
    PyObject *tmp_list_element_1;
    PyObject *tmp_source_name_1;
    PyFrameObject *frame_module;


    // Module code.
    tmp_assign_source_1 = const_str_digest_539b55806ce926f35e1b4324520ef591;
    UPDATE_STRING_DICT0( moduledict_babel, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_babel, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    // Frame without reuse.
    frame_module = MAKE_MODULE_FRAME( codeobj_deefa2ace9ef29b89b1b29eecf0a7474, module_babel );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_module );
    assert( Py_REFCNT( frame_module ) == 1 );

#if PYTHON_VERSION >= 340
    frame_module->f_executing += 1;
#endif

    // Framed code:
    tmp_assign_source_3 = PyList_New( 1 );
    tmp_source_name_1 = PyObject_GetAttrString(PyImport_ImportModule("os"), "path");
    if ( tmp_source_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );


        goto frame_exception_exit_1;
    }
    tmp_called_name_1 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_dirname );
    if ( tmp_called_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );


        goto frame_exception_exit_1;
    }
    tmp_args_element_name_1 = module_filename_obj;
    {
        PyObject *call_args[] = { tmp_args_element_name_1 };
        tmp_list_element_1 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_1, call_args );
    }

    Py_DECREF( tmp_called_name_1 );
    if ( tmp_list_element_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );
        Py_DECREF( tmp_assign_source_3 );


        goto frame_exception_exit_1;
    }
    PyList_SET_ITEM( tmp_assign_source_3, 0, tmp_list_element_1 );
    UPDATE_STRING_DICT1( moduledict_babel, (Nuitka_StringObject *)const_str_plain___path__, tmp_assign_source_3 );
    tmp_assign_source_4 = Py_None;
    UPDATE_STRING_DICT0( moduledict_babel, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_4 );
    tmp_assign_source_5 = const_str_plain_babel;
    UPDATE_STRING_DICT0( moduledict_babel, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_5 );
    tmp_import_globals_1 = ((PyModuleObject *)module_babel)->md_dict;
    frame_module->f_lineno = 20;
    tmp_import_name_from_1 = IMPORT_MODULE( const_str_digest_34fba4047b17e32647652cd9e29451c9, tmp_import_globals_1, tmp_import_globals_1, const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, const_int_0 );
    if ( tmp_import_name_from_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_6 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_UnknownLocaleError );
    Py_DECREF( tmp_import_name_from_1 );
    if ( tmp_assign_source_6 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_babel, (Nuitka_StringObject *)const_str_plain_UnknownLocaleError, tmp_assign_source_6 );
    tmp_import_globals_2 = ((PyModuleObject *)module_babel)->md_dict;
    frame_module->f_lineno = 20;
    tmp_import_name_from_2 = IMPORT_MODULE( const_str_digest_34fba4047b17e32647652cd9e29451c9, tmp_import_globals_2, tmp_import_globals_2, const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, const_int_0 );
    if ( tmp_import_name_from_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_7 = IMPORT_NAME( tmp_import_name_from_2, const_str_plain_Locale );
    Py_DECREF( tmp_import_name_from_2 );
    if ( tmp_assign_source_7 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_babel, (Nuitka_StringObject *)const_str_plain_Locale, tmp_assign_source_7 );
    tmp_import_globals_3 = ((PyModuleObject *)module_babel)->md_dict;
    frame_module->f_lineno = 20;
    tmp_import_name_from_3 = IMPORT_MODULE( const_str_digest_34fba4047b17e32647652cd9e29451c9, tmp_import_globals_3, tmp_import_globals_3, const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, const_int_0 );
    if ( tmp_import_name_from_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_8 = IMPORT_NAME( tmp_import_name_from_3, const_str_plain_default_locale );
    Py_DECREF( tmp_import_name_from_3 );
    if ( tmp_assign_source_8 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_babel, (Nuitka_StringObject *)const_str_plain_default_locale, tmp_assign_source_8 );
    tmp_import_globals_4 = ((PyModuleObject *)module_babel)->md_dict;
    frame_module->f_lineno = 20;
    tmp_import_name_from_4 = IMPORT_MODULE( const_str_digest_34fba4047b17e32647652cd9e29451c9, tmp_import_globals_4, tmp_import_globals_4, const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, const_int_0 );
    if ( tmp_import_name_from_4 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_9 = IMPORT_NAME( tmp_import_name_from_4, const_str_plain_negotiate_locale );
    Py_DECREF( tmp_import_name_from_4 );
    if ( tmp_assign_source_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_babel, (Nuitka_StringObject *)const_str_plain_negotiate_locale, tmp_assign_source_9 );
    tmp_import_globals_5 = ((PyModuleObject *)module_babel)->md_dict;
    frame_module->f_lineno = 20;
    tmp_import_name_from_5 = IMPORT_MODULE( const_str_digest_34fba4047b17e32647652cd9e29451c9, tmp_import_globals_5, tmp_import_globals_5, const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, const_int_0 );
    if ( tmp_import_name_from_5 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_10 = IMPORT_NAME( tmp_import_name_from_5, const_str_plain_parse_locale );
    Py_DECREF( tmp_import_name_from_5 );
    if ( tmp_assign_source_10 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_babel, (Nuitka_StringObject *)const_str_plain_parse_locale, tmp_assign_source_10 );
    tmp_import_globals_6 = ((PyModuleObject *)module_babel)->md_dict;
    frame_module->f_lineno = 20;
    tmp_import_name_from_6 = IMPORT_MODULE( const_str_digest_34fba4047b17e32647652cd9e29451c9, tmp_import_globals_6, tmp_import_globals_6, const_tuple_9b6b57ecfaba7d8f370e4a7a34e338a6_tuple, const_int_0 );
    if ( tmp_import_name_from_6 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_11 = IMPORT_NAME( tmp_import_name_from_6, const_str_plain_get_locale_identifier );
    Py_DECREF( tmp_import_name_from_6 );
    if ( tmp_assign_source_11 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 20;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_babel, (Nuitka_StringObject *)const_str_plain_get_locale_identifier, tmp_assign_source_11 );

    // Restore frame exception if necessary.
#if 0
    RESTORE_FRAME_EXCEPTION( frame_module );
#endif
    popFrameStack();

    assertFrameObject( frame_module );
    Py_DECREF( frame_module );

    goto frame_no_exception_1;
    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_module );
#endif

    if ( exception_tb == NULL )
    {
        exception_tb = MAKE_TRACEBACK( frame_module, exception_lineno );
    }
    else if ( exception_tb->tb_frame != frame_module )
    {
        PyTracebackObject *traceback_new = MAKE_TRACEBACK( frame_module, exception_lineno );
        traceback_new->tb_next = exception_tb;
        exception_tb = traceback_new;
    }

    // Put the previous frame back on top.
    popFrameStack();

#if PYTHON_VERSION >= 340
    frame_module->f_executing -= 1;
#endif
    Py_DECREF( frame_module );

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;
    tmp_assign_source_12 = const_str_digest_e248bf675f752bbffffa3cb66fd59b1a;
    UPDATE_STRING_DICT0( moduledict_babel, (Nuitka_StringObject *)const_str_plain___version__, tmp_assign_source_12 );

    return MOD_RETURN_VALUE( module_babel );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
