// Generated code for Python source for module 'IPython.core.payloadpage'
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

// The _module_IPython$core$payloadpage is a Python object pointer of module type.

// Note: For full compatibility with CPython, every module variable access
// needs to go through it except for cases where the module cannot possibly
// have changed in the mean time.

PyObject *module_IPython$core$payloadpage;
PyDictObject *moduledict_IPython$core$payloadpage;

// The module constants used
extern PyObject *const_str_plain_warn;
extern PyObject *const_str_plain_data;
extern PyObject *const_str_plain_page;
extern PyObject *const_str_plain_source;
extern PyObject *const_str_plain___package__;
static PyObject *const_str_digest_2941dcea19b16a2329d928d274d6a712;
extern PyObject *const_str_plain_strng;
extern PyObject *const_str_plain_warnings;
extern PyObject *const_str_plain_dict;
extern PyObject *const_str_digest_9ef21afda882614b7db2bd2f0eca2fdd;
extern PyObject *const_str_plain_shell;
extern PyObject *const_dict_empty;
extern PyObject *const_str_plain_screen_lines;
extern PyObject *const_str_plain___file__;
extern PyObject *const_str_plain_payload_manager;
static PyObject *const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple;
extern PyObject *const_str_plain_max;
static PyObject *const_tuple_str_plain_corepage_tuple;
extern PyObject *const_int_0;
extern PyObject *const_str_plain_payloadpage;
static PyObject *const_str_digest_85e9b25b658ce37c1b3769aa703b5df9;
extern PyObject *const_str_digest_2896da4659c0e23f2fb0650cde4c9812;
static PyObject *const_str_digest_004cb6d330c52977a277e286e1762f4c;
extern PyObject *const_tuple_int_0_int_0_none_tuple;
static PyObject *const_tuple_str_digest_eb2ff53e18620d565d59b8d415e26fe6_tuple;
extern PyObject *const_tuple_empty;
static PyObject *const_str_digest_b52c3963d6cae95bee20111e9aafe7e7;
extern PyObject *const_str_plain_payload;
static PyObject *const_str_digest_eb2ff53e18620d565d59b8d415e26fe6;
static PyObject *const_str_plain_install_payload_page;
extern PyObject *const_str_plain_pager_cmd;
extern PyObject *const_str_digest_f8a1c9d016d0db16e3b8bcd23c2efa72;
extern PyObject *const_str_plain___loader__;
extern PyObject *const_str_plain_get_ipython;
static PyObject *const_str_digest_f3ef4ad68b573fa26c5d680ad7ecd71a;
extern PyObject *const_tuple_str_plain_page_tuple;
extern PyObject *const_str_plain_start;
static PyObject *const_str_plain_corepage;
extern PyObject *const_tuple_str_plain_get_ipython_tuple;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_plain___cached__;
extern PyObject *const_str_plain_write_payload;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_str_digest_2941dcea19b16a2329d928d274d6a712 = UNSTREAM_STRING( &constant_bin[ 606259 ], 104, 0 );
    const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple = PyTuple_New( 7 );
    PyTuple_SET_ITEM( const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple, 0, const_str_plain_strng ); Py_INCREF( const_str_plain_strng );
    PyTuple_SET_ITEM( const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple, 1, const_str_plain_start ); Py_INCREF( const_str_plain_start );
    PyTuple_SET_ITEM( const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple, 2, const_str_plain_screen_lines ); Py_INCREF( const_str_plain_screen_lines );
    PyTuple_SET_ITEM( const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple, 3, const_str_plain_pager_cmd ); Py_INCREF( const_str_plain_pager_cmd );
    PyTuple_SET_ITEM( const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple, 4, const_str_plain_shell ); Py_INCREF( const_str_plain_shell );
    PyTuple_SET_ITEM( const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple, 5, const_str_plain_data ); Py_INCREF( const_str_plain_data );
    PyTuple_SET_ITEM( const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple, 6, const_str_plain_payload ); Py_INCREF( const_str_plain_payload );
    const_tuple_str_plain_corepage_tuple = PyTuple_New( 1 );
    const_str_plain_corepage = UNSTREAM_STRING( &constant_bin[ 606363 ], 8, 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_corepage_tuple, 0, const_str_plain_corepage ); Py_INCREF( const_str_plain_corepage );
    const_str_digest_85e9b25b658ce37c1b3769aa703b5df9 = UNSTREAM_STRING( &constant_bin[ 606371 ], 24, 0 );
    const_str_digest_004cb6d330c52977a277e286e1762f4c = UNSTREAM_STRING( &constant_bin[ 606395 ], 27, 0 );
    const_tuple_str_digest_eb2ff53e18620d565d59b8d415e26fe6_tuple = PyTuple_New( 1 );
    const_str_digest_eb2ff53e18620d565d59b8d415e26fe6 = UNSTREAM_STRING( &constant_bin[ 606422 ], 110, 0 );
    PyTuple_SET_ITEM( const_tuple_str_digest_eb2ff53e18620d565d59b8d415e26fe6_tuple, 0, const_str_digest_eb2ff53e18620d565d59b8d415e26fe6 ); Py_INCREF( const_str_digest_eb2ff53e18620d565d59b8d415e26fe6 );
    const_str_digest_b52c3963d6cae95bee20111e9aafe7e7 = UNSTREAM_STRING( &constant_bin[ 606532 ], 32, 0 );
    const_str_plain_install_payload_page = UNSTREAM_STRING( &constant_bin[ 606422 ], 20, 1 );
    const_str_digest_f3ef4ad68b573fa26c5d680ad7ecd71a = UNSTREAM_STRING( &constant_bin[ 606564 ], 359, 0 );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_IPython$core$payloadpage( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_18a305393bb3f864dc39773eb59023a8;
static PyCodeObject *codeobj_6bcd4b28161ac4efd4ccd4781448f908;
static PyCodeObject *codeobj_c62c721ed2c5b8e4a92fe59dc93aa2cf;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_004cb6d330c52977a277e286e1762f4c );
    codeobj_18a305393bb3f864dc39773eb59023a8 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_install_payload_page, 43, const_tuple_str_plain_corepage_tuple, 0, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_6bcd4b28161ac4efd4ccd4781448f908 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_page, 11, const_tuple_e97b9f00f64524773bc5c5666f2c06b4_tuple, 4, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_c62c721ed2c5b8e4a92fe59dc93aa2cf = MAKE_CODEOBJ( module_filename_obj, const_str_plain_payloadpage, 1, const_tuple_empty, 0, 0, CO_NOFREE );
}

// The module function declarations.
static PyObject *MAKE_FUNCTION_function_1_page_of_IPython$core$payloadpage( PyObject *defaults );


static PyObject *MAKE_FUNCTION_function_2_install_payload_page_of_IPython$core$payloadpage(  );


// The module function definitions.
static PyObject *impl_function_1_page_of_IPython$core$payloadpage( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_strng = python_pars[ 0 ];
    PyObject *par_start = python_pars[ 1 ];
    PyObject *par_screen_lines = python_pars[ 2 ];
    PyObject *par_pager_cmd = python_pars[ 3 ];
    PyObject *var_shell = NULL;
    PyObject *var_data = NULL;
    PyObject *var_payload = NULL;
    PyObject *exception_type = NULL, *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = -1;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *tmp_args_element_name_1;
    PyObject *tmp_args_element_name_2;
    PyObject *tmp_args_element_name_3;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_assign_source_2;
    PyObject *tmp_assign_source_3;
    PyObject *tmp_assign_source_4;
    PyObject *tmp_assign_source_5;
    PyObject *tmp_called_name_1;
    PyObject *tmp_called_name_2;
    PyObject *tmp_called_name_3;
    PyObject *tmp_dict_key_1;
    PyObject *tmp_dict_key_2;
    PyObject *tmp_dict_key_3;
    PyObject *tmp_dict_key_4;
    PyObject *tmp_dict_value_1;
    PyObject *tmp_dict_value_2;
    PyObject *tmp_dict_value_3;
    PyObject *tmp_dict_value_4;
    PyObject *tmp_frame_locals;
    PyObject *tmp_isinstance_cls_1;
    PyObject *tmp_isinstance_inst_1;
    int tmp_res;
    PyObject *tmp_return_value;
    PyObject *tmp_source_name_1;
    PyObject *tmp_source_name_2;
    NUITKA_MAY_BE_UNUSED PyObject *tmp_unused;
    static PyFrameObject *cache_frame_function = NULL;

    PyFrameObject *frame_function;

    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_function, codeobj_6bcd4b28161ac4efd4ccd4781448f908, module_IPython$core$payloadpage );
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
    tmp_called_name_1 = LOOKUP_BUILTIN( const_str_plain_max );
    assert( tmp_called_name_1 != NULL );
    tmp_args_element_name_1 = const_int_0;
    tmp_args_element_name_2 = par_start;

    frame_function->f_lineno = 28;
    {
        PyObject *call_args[] = { tmp_args_element_name_1, tmp_args_element_name_2 };
        tmp_assign_source_1 = CALL_FUNCTION_WITH_ARGS2( tmp_called_name_1, call_args );
    }

    if ( tmp_assign_source_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 28;
        goto frame_exception_exit_1;
    }
    {
        PyObject *old = par_start;
        assert( old != NULL );
        par_start = tmp_assign_source_1;
        Py_DECREF( old );
    }

    tmp_called_name_2 = GET_STRING_DICT_VALUE( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain_get_ipython );

    if (unlikely( tmp_called_name_2 == NULL ))
    {
        tmp_called_name_2 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_get_ipython );
    }

    if ( tmp_called_name_2 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "get_ipython" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 29;
        goto frame_exception_exit_1;
    }

    frame_function->f_lineno = 29;
    tmp_assign_source_2 = CALL_FUNCTION_NO_ARGS( tmp_called_name_2 );
    if ( tmp_assign_source_2 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 29;
        goto frame_exception_exit_1;
    }
    assert( var_shell == NULL );
    var_shell = tmp_assign_source_2;

    tmp_isinstance_inst_1 = par_strng;

    tmp_isinstance_cls_1 = LOOKUP_BUILTIN( const_str_plain_dict );
    assert( tmp_isinstance_cls_1 != NULL );
    tmp_res = Nuitka_IsInstance( tmp_isinstance_inst_1, tmp_isinstance_cls_1 );
    if ( tmp_res == -1 )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 31;
        goto frame_exception_exit_1;
    }
    if ( tmp_res == 1 )
    {
        goto branch_yes_1;
    }
    else
    {
        goto branch_no_1;
    }
    branch_yes_1:;
    tmp_assign_source_3 = par_strng;

    assert( var_data == NULL );
    Py_INCREF( tmp_assign_source_3 );
    var_data = tmp_assign_source_3;

    goto branch_end_1;
    branch_no_1:;
    tmp_assign_source_4 = _PyDict_NewPresized( 1 );
    tmp_dict_key_1 = const_str_digest_9ef21afda882614b7db2bd2f0eca2fdd;
    tmp_dict_value_1 = par_strng;

    PyDict_SetItem( tmp_assign_source_4, tmp_dict_key_1, tmp_dict_value_1 );
    assert( var_data == NULL );
    var_data = tmp_assign_source_4;

    branch_end_1:;
    tmp_assign_source_5 = _PyDict_NewPresized( 3 );
    tmp_dict_key_2 = const_str_plain_source;
    tmp_dict_value_2 = const_str_plain_page;
    PyDict_SetItem( tmp_assign_source_5, tmp_dict_key_2, tmp_dict_value_2 );
    tmp_dict_key_3 = const_str_plain_data;
    tmp_dict_value_3 = var_data;

    PyDict_SetItem( tmp_assign_source_5, tmp_dict_key_3, tmp_dict_value_3 );
    tmp_dict_key_4 = const_str_plain_start;
    tmp_dict_value_4 = par_start;

    if ( tmp_dict_value_4 == NULL )
    {
        Py_DECREF( tmp_assign_source_5 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "start" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 38;
        goto frame_exception_exit_1;
    }

    PyDict_SetItem( tmp_assign_source_5, tmp_dict_key_4, tmp_dict_value_4 );
    assert( var_payload == NULL );
    var_payload = tmp_assign_source_5;

    tmp_source_name_2 = var_shell;

    tmp_source_name_1 = LOOKUP_ATTRIBUTE( tmp_source_name_2, const_str_plain_payload_manager );
    if ( tmp_source_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 40;
        goto frame_exception_exit_1;
    }
    tmp_called_name_3 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_write_payload );
    Py_DECREF( tmp_source_name_1 );
    if ( tmp_called_name_3 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 40;
        goto frame_exception_exit_1;
    }
    tmp_args_element_name_3 = var_payload;

    if ( tmp_args_element_name_3 == NULL )
    {
        Py_DECREF( tmp_called_name_3 );
        exception_type = PyExc_UnboundLocalError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "local variable '%s' referenced before assignment", "payload" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 40;
        goto frame_exception_exit_1;
    }

    frame_function->f_lineno = 40;
    {
        PyObject *call_args[] = { tmp_args_element_name_3 };
        tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_3, call_args );
    }

    Py_DECREF( tmp_called_name_3 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 40;
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );

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
            if ( par_strng )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_strng,
                    par_strng
                );

                assert( res == 0 );
            }

            if ( par_start )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_start,
                    par_start
                );

                assert( res == 0 );
            }

            if ( par_screen_lines )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_screen_lines,
                    par_screen_lines
                );

                assert( res == 0 );
            }

            if ( par_pager_cmd )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_pager_cmd,
                    par_pager_cmd
                );

                assert( res == 0 );
            }

            if ( var_shell )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_shell,
                    var_shell
                );

                assert( res == 0 );
            }

            if ( var_data )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_data,
                    var_data
                );

                assert( res == 0 );
            }

            if ( var_payload )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_payload,
                    var_payload
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

    tmp_return_value = Py_None;
    Py_INCREF( tmp_return_value );
    goto try_return_handler_1;
    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( function_1_page_of_IPython$core$payloadpage );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    Py_XDECREF( par_strng );
    par_strng = NULL;

    Py_XDECREF( par_start );
    par_start = NULL;

    Py_XDECREF( par_screen_lines );
    par_screen_lines = NULL;

    Py_XDECREF( par_pager_cmd );
    par_pager_cmd = NULL;

    Py_XDECREF( var_shell );
    var_shell = NULL;

    Py_XDECREF( var_data );
    var_data = NULL;

    Py_XDECREF( var_payload );
    var_payload = NULL;

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

    Py_XDECREF( par_strng );
    par_strng = NULL;

    Py_XDECREF( par_start );
    par_start = NULL;

    CHECK_OBJECT( (PyObject *)par_screen_lines );
    Py_DECREF( par_screen_lines );
    par_screen_lines = NULL;

    CHECK_OBJECT( (PyObject *)par_pager_cmd );
    Py_DECREF( par_pager_cmd );
    par_pager_cmd = NULL;

    Py_XDECREF( var_shell );
    var_shell = NULL;

    Py_XDECREF( var_data );
    var_data = NULL;

    Py_XDECREF( var_payload );
    var_payload = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_1_page_of_IPython$core$payloadpage );
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


static PyObject *impl_function_2_install_payload_page_of_IPython$core$payloadpage( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *var_corepage = NULL;
    PyObject *exception_type = NULL, *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = -1;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *tmp_assattr_name_1;
    PyObject *tmp_assattr_target_1;
    PyObject *tmp_assign_source_1;
    PyObject *tmp_called_name_1;
    PyObject *tmp_frame_locals;
    PyObject *tmp_import_globals_1;
    PyObject *tmp_import_locals_1;
    PyObject *tmp_import_name_from_1;
    bool tmp_result;
    PyObject *tmp_return_value;
    PyObject *tmp_source_name_1;
    NUITKA_MAY_BE_UNUSED PyObject *tmp_unused;
    static PyFrameObject *cache_frame_function = NULL;

    PyFrameObject *frame_function;

    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    MAKE_OR_REUSE_FRAME( cache_frame_function, codeobj_18a305393bb3f864dc39773eb59023a8, module_IPython$core$payloadpage );
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
    tmp_source_name_1 = GET_STRING_DICT_VALUE( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain_warnings );

    if (unlikely( tmp_source_name_1 == NULL ))
    {
        tmp_source_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_warnings );
    }

    if ( tmp_source_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "warnings" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 48;
        goto frame_exception_exit_1;
    }

    tmp_called_name_1 = LOOKUP_ATTRIBUTE( tmp_source_name_1, const_str_plain_warn );
    if ( tmp_called_name_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 48;
        goto frame_exception_exit_1;
    }
    frame_function->f_lineno = 50;
    tmp_unused = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_1, &PyTuple_GET_ITEM( const_tuple_str_digest_eb2ff53e18620d565d59b8d415e26fe6_tuple, 0 ) );

    Py_DECREF( tmp_called_name_1 );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 50;
        goto frame_exception_exit_1;
    }
    Py_DECREF( tmp_unused );
    tmp_import_globals_1 = ((PyModuleObject *)module_IPython$core$payloadpage)->md_dict;
    tmp_import_locals_1 = PyDict_New();
    if ( var_corepage )
    {
        int res = PyDict_SetItem(
            tmp_import_locals_1,
            const_str_plain_corepage,
            var_corepage
        );

        assert( res == 0 );
    }

    frame_function->f_lineno = 51;
    tmp_import_name_from_1 = IMPORT_MODULE( const_str_digest_2896da4659c0e23f2fb0650cde4c9812, tmp_import_globals_1, tmp_import_locals_1, const_tuple_str_plain_page_tuple, const_int_0 );
    Py_DECREF( tmp_import_locals_1 );
    if ( tmp_import_name_from_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 51;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_1 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_page );
    Py_DECREF( tmp_import_name_from_1 );
    if ( tmp_assign_source_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 51;
        goto frame_exception_exit_1;
    }
    assert( var_corepage == NULL );
    var_corepage = tmp_assign_source_1;

    tmp_assattr_name_1 = GET_STRING_DICT_VALUE( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain_page );

    if (unlikely( tmp_assattr_name_1 == NULL ))
    {
        tmp_assattr_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_page );
    }

    if ( tmp_assattr_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "page" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 52;
        goto frame_exception_exit_1;
    }

    tmp_assattr_target_1 = var_corepage;

    tmp_result = SET_ATTRIBUTE( tmp_assattr_target_1, const_str_plain_page, tmp_assattr_name_1 );
    if ( tmp_result == false )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 52;
        goto frame_exception_exit_1;
    }

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
            if ( var_corepage )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_corepage,
                    var_corepage
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

    tmp_return_value = Py_None;
    Py_INCREF( tmp_return_value );
    goto try_return_handler_1;
    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( function_2_install_payload_page_of_IPython$core$payloadpage );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    Py_XDECREF( var_corepage );
    var_corepage = NULL;

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

    Py_XDECREF( var_corepage );
    var_corepage = NULL;

    // Re-raise.
    exception_type = exception_keeper_type_1;
    exception_value = exception_keeper_value_1;
    exception_tb = exception_keeper_tb_1;
    exception_lineno = exception_keeper_lineno_1;

    goto function_exception_exit;
    // End of try:

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_2_install_payload_page_of_IPython$core$payloadpage );
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



static PyObject *MAKE_FUNCTION_function_1_page_of_IPython$core$payloadpage( PyObject *defaults )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_1_page_of_IPython$core$payloadpage,
        const_str_plain_page,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_6bcd4b28161ac4efd4ccd4781448f908,
        defaults,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_IPython$core$payloadpage,
        const_str_digest_f3ef4ad68b573fa26c5d680ad7ecd71a
    );

    return result;
}



static PyObject *MAKE_FUNCTION_function_2_install_payload_page_of_IPython$core$payloadpage(  )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_2_install_payload_page_of_IPython$core$payloadpage,
        const_str_plain_install_payload_page,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_18a305393bb3f864dc39773eb59023a8,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_IPython$core$payloadpage,
        const_str_digest_2941dcea19b16a2329d928d274d6a712
    );

    return result;
}



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_IPython$core$payloadpage =
{
    PyModuleDef_HEAD_INIT,
    "IPython.core.payloadpage",   /* m_name */
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

MOD_INIT_DECL( IPython$core$payloadpage )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_IPython$core$payloadpage );
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

    // puts( "in initIPython$core$payloadpage" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_IPython$core$payloadpage = Py_InitModule4(
        "IPython.core.payloadpage",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_IPython$core$payloadpage = PyModule_Create( &mdef_IPython$core$payloadpage );
#endif

    moduledict_IPython$core$payloadpage = (PyDictObject *)((PyModuleObject *)module_IPython$core$payloadpage)->md_dict;

    CHECK_OBJECT( module_IPython$core$payloadpage );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_digest_85e9b25b658ce37c1b3769aa703b5df9, module_IPython$core$payloadpage );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    PyObject *module_dict = PyModule_GetDict( module_IPython$core$payloadpage );

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
    PyObject *tmp_defaults_1;
    PyObject *tmp_import_globals_1;
    PyObject *tmp_import_globals_2;
    PyObject *tmp_import_name_from_1;
    PyFrameObject *frame_module;


    // Module code.
    tmp_assign_source_1 = const_str_digest_b52c3963d6cae95bee20111e9aafe7e7;
    UPDATE_STRING_DICT0( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    tmp_assign_source_3 = Py_None;
    UPDATE_STRING_DICT0( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_3 );
    tmp_assign_source_4 = const_str_digest_2896da4659c0e23f2fb0650cde4c9812;
    UPDATE_STRING_DICT0( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_4 );
    // Frame without reuse.
    frame_module = MAKE_MODULE_FRAME( codeobj_c62c721ed2c5b8e4a92fe59dc93aa2cf, module_IPython$core$payloadpage );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_module );
    assert( Py_REFCNT( frame_module ) == 1 );

#if PYTHON_VERSION >= 340
    frame_module->f_executing += 1;
#endif

    // Framed code:
    tmp_import_globals_1 = ((PyModuleObject *)module_IPython$core$payloadpage)->md_dict;
    frame_module->f_lineno = 7;
    tmp_assign_source_5 = IMPORT_MODULE( const_str_plain_warnings, tmp_import_globals_1, tmp_import_globals_1, Py_None, const_int_0 );
    if ( tmp_assign_source_5 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 7;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain_warnings, tmp_assign_source_5 );
    tmp_import_globals_2 = ((PyModuleObject *)module_IPython$core$payloadpage)->md_dict;
    frame_module->f_lineno = 8;
    tmp_import_name_from_1 = IMPORT_MODULE( const_str_digest_f8a1c9d016d0db16e3b8bcd23c2efa72, tmp_import_globals_2, tmp_import_globals_2, const_tuple_str_plain_get_ipython_tuple, const_int_0 );
    if ( tmp_import_name_from_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 8;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_6 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_get_ipython );
    Py_DECREF( tmp_import_name_from_1 );
    if ( tmp_assign_source_6 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 8;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain_get_ipython, tmp_assign_source_6 );

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
    tmp_defaults_1 = const_tuple_int_0_int_0_none_tuple;
    tmp_assign_source_7 = MAKE_FUNCTION_function_1_page_of_IPython$core$payloadpage( INCREASE_REFCOUNT( tmp_defaults_1 ) );
    UPDATE_STRING_DICT1( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain_page, tmp_assign_source_7 );
    tmp_assign_source_8 = MAKE_FUNCTION_function_2_install_payload_page_of_IPython$core$payloadpage(  );
    UPDATE_STRING_DICT1( moduledict_IPython$core$payloadpage, (Nuitka_StringObject *)const_str_plain_install_payload_page, tmp_assign_source_8 );

    return MOD_RETURN_VALUE( module_IPython$core$payloadpage );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
