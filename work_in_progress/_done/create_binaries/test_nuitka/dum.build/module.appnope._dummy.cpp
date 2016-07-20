// Generated code for Python source for module 'appnope._dummy'
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

// The _module_appnope$_dummy is a Python object pointer of module type.

// Note: For full compatibility with CPython, every module variable access
// needs to go through it except for cases where the module cannot possibly
// have changed in the mean time.

PyObject *module_appnope$_dummy;
PyDictObject *moduledict_appnope$_dummy;

// The module constants used
extern PyObject *const_str_plain_options;
extern PyObject *const_str_plain___package__;
extern PyObject *const_str_plain_contextmanager;
extern PyObject *const_str_plain_nope;
extern PyObject *const_str_digest_8716175da5d8b952a007edfc8eace7a7;
extern PyObject *const_tuple_str_empty_tuple;
extern PyObject *const_str_plain_napping_allowed;
extern PyObject *const_dict_empty;
extern PyObject *const_str_plain___file__;
static PyObject *const_tuple_str_plain_activity_tuple;
extern PyObject *const_int_0;
static PyObject *const_tuple_int_0_str_digest_8716175da5d8b952a007edfc8eace7a7_tuple;
extern PyObject *const_str_plain___doc__;
extern PyObject *const_str_plain_activity;
extern PyObject *const_str_plain_endActivity;
extern PyObject *const_str_plain__dummy;
extern PyObject *const_str_plain_nap;
extern PyObject *const_tuple_empty;
extern PyObject *const_tuple_str_plain_options_str_plain_reason_tuple;
extern PyObject *const_str_plain_contextlib;
static PyObject *const_str_digest_92029ad792fd39eaee6ec9b7de5303c7;
extern PyObject *const_str_plain___loader__;
extern PyObject *const_str_plain_appnope;
extern PyObject *const_str_empty;
static PyObject *const_str_digest_0d56ce4310ccd298b36bcc745e829049;
extern PyObject *const_tuple_str_plain_contextmanager_tuple;
extern PyObject *const_str_plain_nope_scope;
extern PyObject *const_str_plain___cached__;
extern PyObject *const_str_plain_reason;
extern PyObject *const_str_plain_beginActivityWithOptions;
static PyObject *module_filename_obj;

static bool constants_created = false;

static void createModuleConstants( void )
{
    const_tuple_str_plain_activity_tuple = PyTuple_New( 1 );
    PyTuple_SET_ITEM( const_tuple_str_plain_activity_tuple, 0, const_str_plain_activity ); Py_INCREF( const_str_plain_activity );
    const_tuple_int_0_str_digest_8716175da5d8b952a007edfc8eace7a7_tuple = PyTuple_New( 2 );
    PyTuple_SET_ITEM( const_tuple_int_0_str_digest_8716175da5d8b952a007edfc8eace7a7_tuple, 0, const_int_0 ); Py_INCREF( const_int_0 );
    PyTuple_SET_ITEM( const_tuple_int_0_str_digest_8716175da5d8b952a007edfc8eace7a7_tuple, 1, const_str_digest_8716175da5d8b952a007edfc8eace7a7 ); Py_INCREF( const_str_digest_8716175da5d8b952a007edfc8eace7a7 );
    const_str_digest_92029ad792fd39eaee6ec9b7de5303c7 = UNSTREAM_STRING( &constant_bin[ 925139 ], 17, 0 );
    const_str_digest_0d56ce4310ccd298b36bcc745e829049 = UNSTREAM_STRING( &constant_bin[ 925156 ], 14, 0 );

    constants_created = true;
}

#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_appnope$_dummy( void )
{
    // The module may not have been used at all.
    if (constants_created == false) return;


}
#endif

// The module code objects.
static PyCodeObject *codeobj_e02d9111784e4c58c8aa0e30844d106c;
static PyCodeObject *codeobj_7eef5dec5d02fd780260455589382c19;
static PyCodeObject *codeobj_44dfaeacd44d2003c8a06ce2b29d0e48;
static PyCodeObject *codeobj_2441dd112d2387095220027827a71fea;
static PyCodeObject *codeobj_8c45ea6d54ca47d69dfd54273e8e67a1;
static PyCodeObject *codeobj_bec8c53b2fa7c87a686840775b8636f0;
static PyCodeObject *codeobj_a7dbba9722bd8174116fa6607e3ea47b;
static PyCodeObject *codeobj_4bc4f35a8561aea6b9191a4286629083;

static void createModuleCodeObjects(void)
{
    module_filename_obj = MAKE_RELATIVE_PATH( const_str_digest_92029ad792fd39eaee6ec9b7de5303c7 );
    codeobj_e02d9111784e4c58c8aa0e30844d106c = MAKE_CODEOBJ( module_filename_obj, const_str_plain__dummy, 1, const_tuple_empty, 0, 0, CO_NOFREE );
    codeobj_7eef5dec5d02fd780260455589382c19 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_beginActivityWithOptions, 9, const_tuple_str_plain_options_str_plain_reason_tuple, 2, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_44dfaeacd44d2003c8a06ce2b29d0e48 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_endActivity, 12, const_tuple_str_plain_activity_tuple, 1, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_2441dd112d2387095220027827a71fea = MAKE_CODEOBJ( module_filename_obj, const_str_plain_nap, 18, const_tuple_empty, 0, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_8c45ea6d54ca47d69dfd54273e8e67a1 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_napping_allowed, 29, const_tuple_empty, 0, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_bec8c53b2fa7c87a686840775b8636f0 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_nope, 15, const_tuple_empty, 0, 0, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_a7dbba9722bd8174116fa6607e3ea47b = MAKE_CODEOBJ( module_filename_obj, const_str_plain_nope_scope, 22, const_tuple_str_plain_options_str_plain_reason_tuple, 2, 0, CO_GENERATOR | CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE );
    codeobj_4bc4f35a8561aea6b9191a4286629083 = MAKE_CODEOBJ( module_filename_obj, const_str_plain_nope_scope, 22, const_tuple_str_plain_options_str_plain_reason_tuple, 2, 0, CO_GENERATOR | CO_OPTIMIZED | CO_NEWLOCALS );
}

// The module function declarations.
static void genobj_1_nope_scope_of_function_5_nope_scope_of_appnope$_dummy_context( Nuitka_GeneratorObject *generator );


static PyObject *MAKE_FUNCTION_function_1_beginActivityWithOptions_of_appnope$_dummy( PyObject *defaults );


static PyObject *MAKE_FUNCTION_function_2_endActivity_of_appnope$_dummy(  );


static PyObject *MAKE_FUNCTION_function_3_nope_of_appnope$_dummy(  );


static PyObject *MAKE_FUNCTION_function_4_nap_of_appnope$_dummy(  );


static PyObject *MAKE_FUNCTION_function_5_nope_scope_of_appnope$_dummy( PyObject *defaults );


static PyObject *MAKE_FUNCTION_function_6_napping_allowed_of_appnope$_dummy(  );


// The module function definitions.
static PyObject *impl_function_1_beginActivityWithOptions_of_appnope$_dummy( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_options = python_pars[ 0 ];
    PyObject *par_reason = python_pars[ 1 ];
    PyObject *tmp_return_value;
    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    tmp_return_value = Py_None;
    Py_INCREF( tmp_return_value );
    goto try_return_handler_1;
    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( function_1_beginActivityWithOptions_of_appnope$_dummy );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    CHECK_OBJECT( (PyObject *)par_options );
    Py_DECREF( par_options );
    par_options = NULL;

    CHECK_OBJECT( (PyObject *)par_reason );
    Py_DECREF( par_reason );
    par_reason = NULL;

    goto function_return_exit;
    // End of try:
    CHECK_OBJECT( (PyObject *)par_options );
    Py_DECREF( par_options );
    par_options = NULL;

    CHECK_OBJECT( (PyObject *)par_reason );
    Py_DECREF( par_reason );
    par_reason = NULL;


    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_1_beginActivityWithOptions_of_appnope$_dummy );
    return NULL;

    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}


static PyObject *impl_function_2_endActivity_of_appnope$_dummy( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_activity = python_pars[ 0 ];
    PyObject *tmp_return_value;
    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    tmp_return_value = Py_None;
    Py_INCREF( tmp_return_value );
    goto try_return_handler_1;
    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( function_2_endActivity_of_appnope$_dummy );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    CHECK_OBJECT( (PyObject *)par_activity );
    Py_DECREF( par_activity );
    par_activity = NULL;

    goto function_return_exit;
    // End of try:
    CHECK_OBJECT( (PyObject *)par_activity );
    Py_DECREF( par_activity );
    par_activity = NULL;


    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_2_endActivity_of_appnope$_dummy );
    return NULL;

    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}


static PyObject *impl_function_3_nope_of_appnope$_dummy( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *tmp_return_value;
    tmp_return_value = NULL;

    // Actual function code.
    tmp_return_value = Py_None;
    Py_INCREF( tmp_return_value );
    goto function_return_exit;

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_3_nope_of_appnope$_dummy );
    return NULL;

    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}


static PyObject *impl_function_4_nap_of_appnope$_dummy( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *tmp_return_value;
    tmp_return_value = NULL;

    // Actual function code.
    tmp_return_value = Py_None;
    Py_INCREF( tmp_return_value );
    goto function_return_exit;

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_4_nap_of_appnope$_dummy );
    return NULL;

    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}


static PyObject *impl_function_5_nope_scope_of_appnope$_dummy( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_options = python_pars[ 0 ];
    PyObject *par_reason = python_pars[ 1 ];
    PyObject *tmp_return_value;
    tmp_return_value = NULL;

    // Actual function code.
    // Tried code:
    {
        PyCellObject **closure = (PyCellObject **)malloc(2 * sizeof(PyCellObject *));
        closure[0] = PyCell_NEW0( par_options );
        closure[1] = PyCell_NEW0( par_reason );

        tmp_return_value = Nuitka_Generator_New(
            genobj_1_nope_scope_of_function_5_nope_scope_of_appnope$_dummy_context,
            self->m_name,
#if PYTHON_VERSION >= 350
            self->m_qualname,
#endif
            codeobj_4bc4f35a8561aea6b9191a4286629083,
            closure,
            2
        );
    }

    goto try_return_handler_1;
    // tried codes exits in all cases
    NUITKA_CANNOT_GET_HERE( function_5_nope_scope_of_appnope$_dummy );
    return NULL;
    // Return handler code:
    try_return_handler_1:;
    CHECK_OBJECT( (PyObject *)par_options );
    Py_DECREF( par_options );
    par_options = NULL;

    CHECK_OBJECT( (PyObject *)par_reason );
    Py_DECREF( par_reason );
    par_reason = NULL;

    goto function_return_exit;
    // End of try:
    CHECK_OBJECT( (PyObject *)par_options );
    Py_DECREF( par_options );
    par_options = NULL;

    CHECK_OBJECT( (PyObject *)par_reason );
    Py_DECREF( par_reason );
    par_reason = NULL;


    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_5_nope_scope_of_appnope$_dummy );
    return NULL;

    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}



static void genobj_1_nope_scope_of_function_5_nope_scope_of_appnope$_dummy_context( Nuitka_GeneratorObject *generator )
{
    CHECK_OBJECT( (PyObject *)generator );
    assert( Nuitka_Generator_Check( (PyObject *)generator ) );

    // Local variable initialization
    PyObject *exception_type = NULL, *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = -1;
    PyObject *tmp_expression_name_1;
    PyObject *tmp_frame_locals;
    NUITKA_MAY_BE_UNUSED PyObject *tmp_unused;
    static PyFrameObject *cache_frame_generator = NULL;


    // Actual function code.
    MAKE_OR_REUSE_FRAME( cache_frame_generator, codeobj_a7dbba9722bd8174116fa6607e3ea47b, module_appnope$_dummy );
    generator->m_frame = cache_frame_generator;
    Py_INCREF( generator->m_frame );

#if PYTHON_VERSION >= 340
    generator->m_frame->f_gen = (PyObject *)generator;
#endif

    Py_CLEAR( generator->m_frame->f_back );

    generator->m_frame->f_back = PyThreadState_GET()->frame;
    Py_INCREF( generator->m_frame->f_back );

    PyThreadState_GET()->frame = generator->m_frame;
    Py_INCREF( generator->m_frame );

#if PYTHON_VERSION >= 340
    generator->m_frame->f_executing += 1;
#endif

#if PYTHON_VERSION >= 300
    // Accept currently existing exception as the one to publish again when we
    // yield or yield from.

    PyThreadState *thread_state = PyThreadState_GET();

    generator->m_frame->f_exc_type = thread_state->exc_type;
    if ( generator->m_frame->f_exc_type == Py_None ) generator->m_frame->f_exc_type = NULL;
    Py_XINCREF( generator->m_frame->f_exc_type );
    generator->m_frame->f_exc_value = thread_state->exc_value;
    Py_XINCREF( generator->m_frame->f_exc_value );
    generator->m_frame->f_exc_traceback = thread_state->exc_traceback;
    Py_XINCREF( generator->m_frame->f_exc_traceback );
#endif

    // Framed code:
    // Throwing into not started generators is possible. As they don't stand any
    // chance to deal with them, we might as well create traceback on the
    // outside,
    if ( generator->m_exception_type )
    {
        generator->m_yielded = NULL;

        exception_type = generator->m_exception_type;
        generator->m_exception_type = NULL;

        exception_value = generator->m_exception_value;
        generator->m_exception_value = NULL;

        exception_tb = generator->m_exception_tb;;
        generator->m_exception_tb = NULL;

        if (exception_tb == NULL)
        {
            exception_lineno = 22;
            goto frame_exception_exit_1;
        }
        else
        {
            goto function_exception_exit;
        }
    }

    tmp_expression_name_1 = Py_None;
    tmp_unused = YIELD( generator, INCREASE_REFCOUNT( tmp_expression_name_1 ) );
    if ( tmp_unused == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 27;
        goto frame_exception_exit_1;
    }

#if PYTHON_VERSION >= 340
    generator->m_frame->f_executing -= 1;
#endif

#if PYTHON_VERSION >= 300
    Py_CLEAR( generator->m_frame->f_exc_type );
    Py_CLEAR( generator->m_frame->f_exc_value );
    Py_CLEAR( generator->m_frame->f_exc_traceback );
#endif

    Py_DECREF( generator->m_frame );
    goto frame_no_exception_1;

    frame_exception_exit_1:;

    // If it's not an exit exception, consider and create a traceback for it.
    if ( !EXCEPTION_MATCH_GENERATOR( exception_type ) )
    {
        int needs_detach = false;

        if ( exception_tb == NULL )
        {
            exception_tb = MAKE_TRACEBACK( generator->m_frame, exception_lineno );
            needs_detach = true;
        }
        else if ( exception_tb->tb_frame != generator->m_frame )
        {
            PyTracebackObject *traceback_new = MAKE_TRACEBACK( generator->m_frame, exception_lineno );
            traceback_new->tb_next = exception_tb;
            exception_tb = traceback_new;

            needs_detach = true;
        }

        if (needs_detach)
        {

            tmp_frame_locals = PyDict_New();
            if ( generator->m_closure[0]->ob_ref )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_options,
                    generator->m_closure[0]->ob_ref
                );

                assert( res == 0 );
            }

            if ( generator->m_closure[1]->ob_ref )
            {
                int res = PyDict_SetItem(
                    tmp_frame_locals,
                    const_str_plain_reason,
                    generator->m_closure[1]->ob_ref
                );

                assert( res == 0 );
            }



            detachFrame( exception_tb, tmp_frame_locals );
        }
    }

#if PYTHON_VERSION >= 300
    Py_CLEAR( generator->m_frame->f_exc_type );
    Py_CLEAR( generator->m_frame->f_exc_value );
    Py_CLEAR( generator->m_frame->f_exc_traceback );
#endif

    Py_DECREF( generator->m_frame );
    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;


    RESTORE_ERROR_OCCURRED( PyExc_StopIteration, NULL, NULL );
    Py_INCREF( PyExc_StopIteration );

    generator->m_yielded = NULL;
    return;

    function_exception_exit:
    assert( exception_type );
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    generator->m_yielded = NULL;
    return;

}


static PyObject *impl_function_6_napping_allowed_of_appnope$_dummy( Nuitka_FunctionObject const *self, PyObject **python_pars )
{
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *tmp_return_value;
    tmp_return_value = NULL;

    // Actual function code.
    tmp_return_value = Py_True;
    Py_INCREF( tmp_return_value );
    goto function_return_exit;

    // Return statement must have exited already.
    NUITKA_CANNOT_GET_HERE( function_6_napping_allowed_of_appnope$_dummy );
    return NULL;

    function_return_exit:

    CHECK_OBJECT( tmp_return_value );
    assert( had_error || !ERROR_OCCURRED() );
    return tmp_return_value;

}



static PyObject *MAKE_FUNCTION_function_1_beginActivityWithOptions_of_appnope$_dummy( PyObject *defaults )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_1_beginActivityWithOptions_of_appnope$_dummy,
        const_str_plain_beginActivityWithOptions,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_7eef5dec5d02fd780260455589382c19,
        defaults,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_appnope$_dummy,
        Py_None
    );

    return result;
}



static PyObject *MAKE_FUNCTION_function_2_endActivity_of_appnope$_dummy(  )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_2_endActivity_of_appnope$_dummy,
        const_str_plain_endActivity,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_44dfaeacd44d2003c8a06ce2b29d0e48,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_appnope$_dummy,
        Py_None
    );

    return result;
}



static PyObject *MAKE_FUNCTION_function_3_nope_of_appnope$_dummy(  )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_3_nope_of_appnope$_dummy,
        const_str_plain_nope,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_bec8c53b2fa7c87a686840775b8636f0,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_appnope$_dummy,
        Py_None
    );

    return result;
}



static PyObject *MAKE_FUNCTION_function_4_nap_of_appnope$_dummy(  )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_4_nap_of_appnope$_dummy,
        const_str_plain_nap,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_2441dd112d2387095220027827a71fea,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_appnope$_dummy,
        Py_None
    );

    return result;
}



static PyObject *MAKE_FUNCTION_function_5_nope_scope_of_appnope$_dummy( PyObject *defaults )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_5_nope_scope_of_appnope$_dummy,
        const_str_plain_nope_scope,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_a7dbba9722bd8174116fa6607e3ea47b,
        defaults,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_appnope$_dummy,
        Py_None
    );

    return result;
}



static PyObject *MAKE_FUNCTION_function_6_napping_allowed_of_appnope$_dummy(  )
{
    PyObject *result = Nuitka_Function_New(
        impl_function_6_napping_allowed_of_appnope$_dummy,
        const_str_plain_napping_allowed,
#if PYTHON_VERSION >= 330
        NULL,
#endif
        codeobj_8c45ea6d54ca47d69dfd54273e8e67a1,
        NULL,
#if PYTHON_VERSION >= 300
        NULL,
        const_dict_empty,
#endif
        module_appnope$_dummy,
        Py_None
    );

    return result;
}



#if PYTHON_VERSION >= 300
static struct PyModuleDef mdef_appnope$_dummy =
{
    PyModuleDef_HEAD_INIT,
    "appnope._dummy",   /* m_name */
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

MOD_INIT_DECL( appnope$_dummy )
{
#if defined(_NUITKA_EXE) || PYTHON_VERSION >= 300
    static bool _init_done = false;

    // Modules might be imported repeatedly, which is to be ignored.
    if ( _init_done )
    {
        return MOD_RETURN_VALUE( module_appnope$_dummy );
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

    // puts( "in initappnope$_dummy" );

    // Create the module object first. There are no methods initially, all are
    // added dynamically in actual code only.  Also no "__doc__" is initially
    // set at this time, as it could not contain NUL characters this way, they
    // are instead set in early module code.  No "self" for modules, we have no
    // use for it.
#if PYTHON_VERSION < 300
    module_appnope$_dummy = Py_InitModule4(
        "appnope._dummy",       // Module Name
        NULL,                    // No methods initially, all are added
                                 // dynamically in actual module code only.
        NULL,                    // No __doc__ is initially set, as it could
                                 // not contain NUL this way, added early in
                                 // actual code.
        NULL,                    // No self for modules, we don't use it.
        PYTHON_API_VERSION
    );
#else
    module_appnope$_dummy = PyModule_Create( &mdef_appnope$_dummy );
#endif

    moduledict_appnope$_dummy = (PyDictObject *)((PyModuleObject *)module_appnope$_dummy)->md_dict;

    CHECK_OBJECT( module_appnope$_dummy );

// Seems to work for Python2.7 out of the box, but for Python3, the module
// doesn't automatically enter "sys.modules", so do it manually.
#if PYTHON_VERSION >= 300
    {
        int r = PyObject_SetItem( PySys_GetObject( (char *)"modules" ), const_str_digest_0d56ce4310ccd298b36bcc745e829049, module_appnope$_dummy );

        assert( r != -1 );
    }
#endif

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    PyObject *module_dict = PyModule_GetDict( module_appnope$_dummy );

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
    PyObject *tmp_called_name_1;
    PyObject *tmp_defaults_1;
    PyObject *tmp_defaults_2;
    PyObject *tmp_import_globals_1;
    PyObject *tmp_import_name_from_1;
    PyFrameObject *frame_module;


    // Module code.
    tmp_assign_source_1 = Py_None;
    UPDATE_STRING_DICT0( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain___doc__, tmp_assign_source_1 );
    tmp_assign_source_2 = module_filename_obj;
    UPDATE_STRING_DICT0( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain___file__, tmp_assign_source_2 );
    tmp_assign_source_3 = Py_None;
    UPDATE_STRING_DICT0( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain___cached__, tmp_assign_source_3 );
    tmp_assign_source_4 = const_str_plain_appnope;
    UPDATE_STRING_DICT0( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain___package__, tmp_assign_source_4 );
    // Frame without reuse.
    frame_module = MAKE_MODULE_FRAME( codeobj_e02d9111784e4c58c8aa0e30844d106c, module_appnope$_dummy );

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStack( frame_module );
    assert( Py_REFCNT( frame_module ) == 1 );

#if PYTHON_VERSION >= 340
    frame_module->f_executing += 1;
#endif

    // Framed code:
    tmp_import_globals_1 = ((PyModuleObject *)module_appnope$_dummy)->md_dict;
    frame_module->f_lineno = 7;
    tmp_import_name_from_1 = IMPORT_MODULE( const_str_plain_contextlib, tmp_import_globals_1, tmp_import_globals_1, const_tuple_str_plain_contextmanager_tuple, const_int_0 );
    if ( tmp_import_name_from_1 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 7;
        goto frame_exception_exit_1;
    }
    tmp_assign_source_5 = IMPORT_NAME( tmp_import_name_from_1, const_str_plain_contextmanager );
    Py_DECREF( tmp_import_name_from_1 );
    if ( tmp_assign_source_5 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 7;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain_contextmanager, tmp_assign_source_5 );
    tmp_defaults_1 = const_tuple_str_empty_tuple;
    tmp_assign_source_6 = MAKE_FUNCTION_function_1_beginActivityWithOptions_of_appnope$_dummy( INCREASE_REFCOUNT( tmp_defaults_1 ) );
    UPDATE_STRING_DICT1( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain_beginActivityWithOptions, tmp_assign_source_6 );
    tmp_assign_source_7 = MAKE_FUNCTION_function_2_endActivity_of_appnope$_dummy(  );
    UPDATE_STRING_DICT1( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain_endActivity, tmp_assign_source_7 );
    tmp_assign_source_8 = MAKE_FUNCTION_function_3_nope_of_appnope$_dummy(  );
    UPDATE_STRING_DICT1( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain_nope, tmp_assign_source_8 );
    tmp_assign_source_9 = MAKE_FUNCTION_function_4_nap_of_appnope$_dummy(  );
    UPDATE_STRING_DICT1( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain_nap, tmp_assign_source_9 );
    tmp_called_name_1 = GET_STRING_DICT_VALUE( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain_contextmanager );

    if (unlikely( tmp_called_name_1 == NULL ))
    {
        tmp_called_name_1 = GET_STRING_DICT_VALUE( dict_builtin, (Nuitka_StringObject *)const_str_plain_contextmanager );
    }

    if ( tmp_called_name_1 == NULL )
    {

        exception_type = PyExc_NameError;
        Py_INCREF( exception_type );
        exception_value = PyUnicode_FromFormat( "name '%s' is not defined", "contextmanager" );
        exception_tb = NULL;
        NORMALIZE_EXCEPTION( &exception_type, &exception_value, &exception_tb );
        CHAIN_EXCEPTION( exception_value );

        exception_lineno = 22;
        goto frame_exception_exit_1;
    }

    tmp_defaults_2 = const_tuple_int_0_str_digest_8716175da5d8b952a007edfc8eace7a7_tuple;
    tmp_args_element_name_1 = MAKE_FUNCTION_function_5_nope_scope_of_appnope$_dummy( INCREASE_REFCOUNT( tmp_defaults_2 ) );
    frame_module->f_lineno = 22;
    {
        PyObject *call_args[] = { tmp_args_element_name_1 };
        tmp_assign_source_10 = CALL_FUNCTION_WITH_ARGS1( tmp_called_name_1, call_args );
    }

    Py_DECREF( tmp_args_element_name_1 );
    if ( tmp_assign_source_10 == NULL )
    {
        assert( ERROR_OCCURRED() );

        FETCH_ERROR_OCCURRED( &exception_type, &exception_value, &exception_tb );


        exception_lineno = 22;
        goto frame_exception_exit_1;
    }
    UPDATE_STRING_DICT1( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain_nope_scope, tmp_assign_source_10 );

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
    tmp_assign_source_11 = MAKE_FUNCTION_function_6_napping_allowed_of_appnope$_dummy(  );
    UPDATE_STRING_DICT1( moduledict_appnope$_dummy, (Nuitka_StringObject *)const_str_plain_napping_allowed, tmp_assign_source_11 );

    return MOD_RETURN_VALUE( module_appnope$_dummy );
    module_exception_exit:
    RESTORE_ERROR_OCCURRED( exception_type, exception_value, exception_tb );
    return MOD_RETURN_VALUE( NULL );
}
