// Generated code for Python source for module 'Cython.Compiler.Future'
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

// The _module_Cython$Compiler$Future is a Python object pointer of module type.

// Note: For full compatibility with CPython, every module variable access
// needs to go through it except for cases where the module cannot possibly
// have changed in the mean time.

PyObject *module_Cython$Compiler$Future;
PyDictObject *moduledict_Cython$Compiler$Future;

// The module constants used
static PyObject *const_tuple_str_plain_print_function_tuple;
extern PyObject *const_str_plain_Future;
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain___future__;
extern PyObject *const_str_plain_unicode_literals;
static PyObject *const_str_digest_6e62b01fe1760df91ddbb8251b9db7bb;
extern PyObject *const_str_digest_725e8123044bef1b6c84c1319cf2b97a;
extern PyObject *const_dict_empty;
static PyObject *const_tuple_str_plain_absolute_import_tuple;
extern PyObject *const_str_plain___file__;
static PyObject *const_tuple_str_plain_unicode_literals_tuple;
extern PyObject *const_str_plain_object;
extern PyObject *const_str_plain___cached__;
static PyObject *const_str_plain_nested_scopes;
extern PyObject *const_int_0;
static PyObject *const_tuple_str_plain_with_statement_tuple;
extern PyObject *const_str_plain_division;
extern PyObject *const_str_plain___doc__;
static PyObject *const_tuple_str_plain_generator_stop_tuple;
static PyObject *const_str_digest_c72b311be946111096fb7ab91e0dde30;
extern PyObject *const_str_plain_generator_stop;
static PyObject *const_tuple_str_plain_generators_tuple;
extern PyObject *const_str_plain_with_statement;
extern PyObject *const_tuple_empty;
static PyObject *const_tuple_str_plain_division_tuple;
static PyObject *const_str_plain_generators;
static PyObject *const_tuple_str_plain_name_str_plain___future___tuple;
extern PyObject *const_str_plain___loader__;
static PyObject *const_str_plain__get_feature;
extern PyObject *const_str_plain_name;
extern PyObject *const_str_plain_absolute_import;
static PyObject *const_tuple_str_plain_nested_scopes_tuple;
extern PyObject *const_str_plain_print_function;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_tuple_str_plain_print_function_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_print_function_tuple, 0, const_str_plain_print_function ); Py_INCREF( const_str_plain_print_function );
    const_str_digest_6e62b01fe1760df91ddbb8251b9db7bb = UNSTREAM_STRING( &constant_bin[ 107393 ], 25, 0 );
    const_tuple_str_plain_absolute_import_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_absolute_import_tuple, 0, const_str_plain_absolute_import ); Py_INCREF( const_str_plain_absolute_import );
    const_tuple_str_plain_unicode_literals_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_unicode_literals_tuple, 0, const_str_plain_unicode_literals ); Py_INCREF( const_str_plain_unicode_literals );
    const_str_plain_nested_scopes = UNSTREAM_STRING( &constant_bin[ 107418 ], 13, 1 );
    const_tuple_str_plain_with_statement_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_with_statement_tuple, 0, const_str_plain_with_statement ); Py_INCREF( const_str_plain_with_statement );
    const_tuple_str_plain_generator_stop_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_generator_stop_tuple, 0, const_str_plain_generator_stop ); Py_INCREF( const_str_plain_generator_stop );
    const_str_digest_c72b311be946111096fb7ab91e0dde30 = UNSTREAM_STRING( &constant_bin[ 107431 ], 22, 0 );
    const_tuple_str_plain_generators_tuple = PyTuple_New( 1 );
    const_str_plain_generators = UNSTREAM_STRING( &constant_bin[ 107453 ], 10, 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_generators_tuple, 0, const_str_plain_generators ); Py_INCREF( const_str_plain_generators );
    const_tuple_str_plain_division_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_division_tuple, 0, const_str_plain_division ); Py_INCREF( const_str_plain_division );
    const_tuple_str_plain_name_str_plain___future___tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_str_plain_name_str_plain___future___tuple, 0, const_str_plain_name ); Py_INCREF( const_str_plain_name );
    PyTuple_SET_ITEM( const_tuple_str_plain_name_str_plain___future___tuple, 1, const_str_plain___future__ ); Py_INCREF( const_str_plain___future__ );
    const_str_plain__get_feature = UNSTREAM_STRING( &constant_bin[ 63 ], 12, 1 );
    const_tuple_str_plain_nested_scopes_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_nested_scopes_tuple, 0, const_str_plain_nested_scopes ); Py_INCREF( const_str_plain_nested_scopes );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_Cython$Compiler$Future( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_0d5b6239147da7eba237ce63ba1ecbee;
static PyCodeObject *codeobj_d6a458164ceeffbaf37e6f8fe8c4ae0a;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_6e62b01fe1760df91ddbb8251b9db7bb );
    codeobj_0d5b6239147da7eba237ce63ba1ecbee = MAKE_CODEOBJ( module_filename_obj, const_str_plain_Future, 1, const_tuple_empty, 0, 0, CO_NOFREE );
    codeobj_d6a458164ceeffbaf37e6f8fe8c4ae0a = MAKE_CODEOBJ( module_filename_obj, const_str_plain__get_feature, 1, const_tuple_str_plain_name_str_plain___future___tuple, 1, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
}

// The module function declarations.
static PyObject *MAKE_FUNCTION_function_1__get_feature_of_Cython$Compiler$Future(  );


// The module function definitions.
static PyObject *impl_function_1__get_feature_of_Cython$Compiler$Future( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_name = python_pars[ 0 ];
    PyObject *var___future__ = NULL;
    PyObject *exception_type = NULL, *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = -1;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_called_name_1;
    PyObject *tmp_frame_locals;
    PyObject *tmp_getattr_attr_1;
    PyObject *tmp_getattr_default_1;
    PyObject *tmp_getattr_target_1;
    PyObject *tmp_import_globals_1;
    PyObject *tmp_import_locals_1;
    PyObject *tmp_return_value;
    static PyFrameObject *cache_frame_function = NULL;

    PyFrameObject *frame_function;

    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_function, codeobj_d6a458164ceeffbaf37e6f8fe8c4ae0a, module_Cython$Compiler$Future );
    frame_function = cache_frame_function;

    // Push the new frame as the currently active one.
    pushFrameStack( frame_function );

    // Mark the frame object as in use, ref count 1 will be up for reuse.
    Py_INCREF( frame_function );
    assert( Py_REFCNT( frame_function ) == 2 ); // Frame stack

#if PYTHON_VERSION >= 340
    frame_function->f_executing += 1;
#endif

    // Framed code:
    tmp_import_globals_1 = ((PyModuleObject *)module_Cython$Compiler$Future)->md_dict;
    tmp_import_locals_1 = PyDict_New();
    if ( par_name )
    {
        int res = PyDict_SetItem(
            tmp_import_locals_1,
            const_str_plain_name,
            par_name
        );

        assert( res == 0 );
    }

    if ( var___future__ )
    {
        int res = PyDict_SetItem(
            tmp_import_locals_1,
            const_str_plain___future__,
            var___future__
        );

        assert( res == 0 );
    }

    frame_function->f_lineno = 2;
    tmp_assign_source_1 = IMPORT_MODULE( const_str_plain___future__, tmp_import_globals_1, tmp_import_locals_1, Py_None, const_int_0 );
    Py_DECREF( tmp_import_locals_1 );
    if ( tmp_assign_source_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 2;
        goto frame_exception_exit_1;
    }
    assert( var___future__ == NULL );
    var___future__ = tmp_assign_source_1;

    tmp_getattr_target_1 = var___future__;

    tmp_getattr_attr_1 = par_name;

    tmp_called_name_1 = LOOKUP_BUILTIN( const_str_plain_object );
    assert( tmp_called_name_1 != NULL );
    frame_function->f_lineno = 4;
    tmp_getattr_default_1 = CALL_FUNCTION_NO_ARGS( tmp_called_name_1 );
    if ( tmp_getattr_default_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 4;
        goto frame_exception_exit_1;
    }
    tmp_return_value = BUILTIN_GETATTR( tmp_getattr_target_1, tmp_getattr_attr_1, tmp_getattr_default_1 );
    Py_DECREF( tmp_getattr_default_1 );
    if ( tmp_return_value == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 4;
        goto frame_exception_exit_1;
    }
    goto frame_return_exit_1;

#if 0
    RESTORE_FRAME_EXCEPTION( frame_function );
#endif
    // Put the previous frame back on top.
    popFrameStack();
#if PYTHON_VERSION >= 340
    frame_function->f_executing -= 1;
#endif
    Py_DECREF( frame_function );
    goto frame_no_exception_1;

    frame_return_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_function );
#endif
    popFrameStack();
#if PYTHON_VERSION >= 340
    frame_function->f_executing -= 1;
#endif
    Py_DECREF( frame_function );
    goto try_return_handler_1;

    frame_exception_exit_1:;
#if 0
    RESTORE_FRAME_EXCEPTION( frame_function );
#endif

    {
        bool needs_detach = false;

        if ( exception_tb == NULL )
        {
            exception_tb = MAKE_TRACEBACK( frame_function, exception_lineno );
            needs_detach = true;
        }
        else if ( exception_lineno != -1 )
        {
            PyTracebackObject *traceback_new = MAKE_TRACEBACK( frame_function, exception_lineno );
            traceback_new->tb_next = exception_tb;
            exception_tb = traceback_new;

            needs_detach = true;
        }

        if (needs_detach)
        {

            tmp_frame_locals = PyDict_New();
            if ( par_name )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_name,
                    par_name
                );

                assert( res == 0 );
            }

            if ( var___future__ )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain___future__,
                    var___future__
                );

                assert( res == 0 );
            }



            detachFrame( exception_tb, tmp_frame_locals );
        }
    }

    popFrameStack();

#if PYTHON_VERSION >= 340
    frame_function->f_executing -= 1;
#endif
    Py_DECREF( frame_function );

    // Return the error.
    goto try_except_handler_1;

    frame_no_exception_1:;

    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( function_1__get_feature_of_Cython$Compiler$Future );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    CHECK_OBJECT( (PyObject *)par_name );
    Py_DECREF( par_name );
    par_name = NULL;

    Py_XDECREF( var___future__ );
    var___future__ = NULL;

    goto function_return_exit;
    // Exception handler code:
    try_except_handler_1:;
    exception_keeper_type_1 = exception_type;
    exception_keeper_value_1 = exception_value;
    exception_keeper_tb_1 = exception_tb;
    exception_keeper_lineno_1 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = -1;

    CHECK_OBJECT( (PyObject *)par_name );
    Py_DECREF( par_name );
    par_name = NULL;

    Py_XDECREF( var___future__ );
    var___future__ = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_1__get_feature_of_Cython$Compiler$Future );
    return NULL;

function_exception_exit:
    assert( exception_type );
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );

    return NULL;
    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}



static PyObject *MAKE_FUNCTION_function_1__get_feature_of_Cython$Compiler$Future(  )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_1__get_feature_of_Cython$Compiler$Future,
        const_str_plain__get_feature,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_d6a458164ceeffbaf37e6f8fe8c4ae0a,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_Cython$Compiler$Future,
        Py_None
    );

    return result;
}



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_Cython$Compiler$Future =
{
    PyModuleDef_HEAD_INIT,
    "Cython.Compiler.Future",   /* m_name */
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

MOD_INIT_DECL( Cython$Compiler$Future )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_Cython$Compiler$Future );
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

    // puts( "in initCython$Compiler$Future" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_Cython$Compiler$Future = Py_InitModule4(
        "Cython.Compiler.Future",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_Cython$Compiler$Future = PyModule_Create( &mdef_Cython$Compiler$Future );
#endif

    moduledict_Cython$Compiler$Future = (PyDictObject *)((PyModuleObject *)module_Cython$Compiler$Future)->md_dict;

    CHECK_OBJECT( module_Cython$Compiler$Future );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_digest_c72b311be946111096fb7ab91e0dde30, module_Cython$Compiler$Future );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    PyObject *module_dict = PyModule_GetDict( module_Cython$Compiler$Future );

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
    PyObject *tmp_assign_source_13;
    PyObject *tmp_called_name_1;
    PyObject *tmp_called_name_2;
    PyObject *tmp_called_name_3;
    PyObject *tmp_called_name_4;
    PyObject *tmp_called_name_5;
    PyObject *tmp_called_name_6;
    PyObject *tmp_called_name_7;
    PyObject *tmp_called_name_8;
    int tmp_res;
    PyFrameObject *frame_module;


    // Module code.
    tmp_assign_source_1 = Py_None;
    UPDATE_STRING_DICT0( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    tmp_assign_source_3 = Py_None;
    UPDATE_STRING_DICT0( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_3 );
    tmp_assign_source_4 = const_str_digest_725e8123044bef1b6c84c1319cf2b97a;
    UPDATE_STRING_DICT0( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_4 );
    tmp_assign_source_5 = MAKE_FUNCTION_function_1__get_feature_of_Cython$Compiler$Future(  );
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature, tmp_assign_source_5 );
    // Frame without reuse.
    frame_module = MAKE_MODULE_FRAME( codeobj_0d5b6239147da7eba237ce63ba1ecbee, module_Cython$Compiler$Future );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_module );
    assert( Py_REFCNT( frame_module ) == 1 );

#if PYTHON_VERSION >= 340
    frame_module->f_executing += 1;
#endif

    // Framed code:
    tmp_called_name_1 = GET_STRING_DICT_VALUE( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature );

    if (unlikely( tmp_called_name_1 == NULL ))
    {
        tmp_called_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__get_feature );
    }

    if ( tmp_called_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_get_feature" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 6;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 6;
    tmp_assign_source_6 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_1, &PyTuple_GET_ITEM( const_tuple_str_plain_unicode_literals_tuple, 0 ) );

    if ( tmp_assign_source_6 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 6;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain_unicode_literals, tmp_assign_source_6 );
    tmp_called_name_2 = GET_STRING_DICT_VALUE( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature );

    if (unlikely( tmp_called_name_2 == NULL ))
    {
        tmp_called_name_2 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__get_feature );
    }

    if ( tmp_called_name_2 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_get_feature" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 7;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 7;
    tmp_assign_source_7 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_2, &PyTuple_GET_ITEM( const_tuple_str_plain_with_statement_tuple, 0 ) );

    if ( tmp_assign_source_7 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 7;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain_with_statement, tmp_assign_source_7 );
    tmp_called_name_3 = GET_STRING_DICT_VALUE( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature );

    if (unlikely( tmp_called_name_3 == NULL ))
    {
        tmp_called_name_3 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__get_feature );
    }

    if ( tmp_called_name_3 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_get_feature" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 8;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 8;
    tmp_assign_source_8 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_3, &PyTuple_GET_ITEM( const_tuple_str_plain_division_tuple, 0 ) );

    if ( tmp_assign_source_8 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 8;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain_division, tmp_assign_source_8 );
    tmp_called_name_4 = GET_STRING_DICT_VALUE( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature );

    if (unlikely( tmp_called_name_4 == NULL ))
    {
        tmp_called_name_4 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__get_feature );
    }

    if ( tmp_called_name_4 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_get_feature" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 9;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 9;
    tmp_assign_source_9 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_4, &PyTuple_GET_ITEM( const_tuple_str_plain_print_function_tuple, 0 ) );

    if ( tmp_assign_source_9 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 9;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain_print_function, tmp_assign_source_9 );
    tmp_called_name_5 = GET_STRING_DICT_VALUE( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature );

    if (unlikely( tmp_called_name_5 == NULL ))
    {
        tmp_called_name_5 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__get_feature );
    }

    if ( tmp_called_name_5 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_get_feature" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 10;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 10;
    tmp_assign_source_10 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_5, &PyTuple_GET_ITEM( const_tuple_str_plain_absolute_import_tuple, 0 ) );

    if ( tmp_assign_source_10 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 10;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain_absolute_import, tmp_assign_source_10 );
    tmp_called_name_6 = GET_STRING_DICT_VALUE( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature );

    if (unlikely( tmp_called_name_6 == NULL ))
    {
        tmp_called_name_6 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__get_feature );
    }

    if ( tmp_called_name_6 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_get_feature" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 11;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 11;
    tmp_assign_source_11 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_6, &PyTuple_GET_ITEM( const_tuple_str_plain_nested_scopes_tuple, 0 ) );

    if ( tmp_assign_source_11 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 11;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain_nested_scopes, tmp_assign_source_11 );
    tmp_called_name_7 = GET_STRING_DICT_VALUE( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature );

    if (unlikely( tmp_called_name_7 == NULL ))
    {
        tmp_called_name_7 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__get_feature );
    }

    if ( tmp_called_name_7 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_get_feature" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 12;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 12;
    tmp_assign_source_12 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_7, &PyTuple_GET_ITEM( const_tuple_str_plain_generators_tuple, 0 ) );

    if ( tmp_assign_source_12 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 12;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain_generators, tmp_assign_source_12 );
    tmp_called_name_8 = GET_STRING_DICT_VALUE( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain__get_feature );

    if (unlikely( tmp_called_name_8 == NULL ))
    {
        tmp_called_name_8 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain__get_feature );
    }

    if ( tmp_called_name_8 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "_get_feature" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 13;
        goto frame_exception_exit_1;
    }

    frame_module->f_lineno = 13;
    tmp_assign_source_13 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_8, &PyTuple_GET_ITEM( const_tuple_str_plain_generator_stop_tuple, 0 ) );

    if ( tmp_assign_source_13 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 13;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_Cython$Compiler$Future, (Nuitka_StringObject *)const_str_plain_generator_stop, tmp_assign_source_13 );
    tmp_res = PyDict_DelItem( (PyObject *)moduledict_Cython$Compiler$Future, const_str_plain__get_feature );
    if ( tmp_res == -1 ) CLEAR_ERROR_OCCURRED();

    if ( tmp_res == -1 )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = UNSTREAM_STRING( &constant_bin[ 57 ], 34, 0 );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 15;
        goto frame_exception_exit_1;
    }


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

    return MOD_RETURN_VALUE( module_Cython$Compiler$Future );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
