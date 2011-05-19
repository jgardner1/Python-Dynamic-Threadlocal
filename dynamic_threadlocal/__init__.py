"""Usage:

If you simply want to access dynamic variables, then use the 'dynamic' value
in this module.

    from dynamic_threadlocal import dynamic

    def foo():
        return dynamic.bar

If you want to assign dynamic variables, then you need to use the 'with'
syntax, described below.

    def baz():
        with dynamic(bar=1):
            return foo() # Always 1

If you want to re-assign or assign new variables to the scope:

    def boo():
        with dynamic() as dyn_scope:
            print baz() # 1
            dyn_scope.bar = 2
            print foo() # 2
            print baz() # 1
            print foo() # 2
            del dyn_scope.bar
            print baz() # 1
            print foo() # NameError

Clearing up misconceptions:

A lot of people on the internet that blog about Python clearly don't
understand what Dynamic Scoping is. If they haven't used perl's "local"
feature or dealt with Lisp's dynamic scoping, they wouldn't understand what
Dynamic Scoping really is. If you are one of those folks, I suggest reading
about perl's "local" or Lisp's dynamic scoping.

FAQ:

Q: What is Dynamic Scoping?
A: Dynamic Scoping allows you to specify variables that are available to
functions you call, and functions they call. This is different from Lexical
Scoping (aka Static Scoping) which doesn't care how a function is called.
Lexical Scoping just looks for where the function was originally defined to
find its missing variables.

Q: Why is this useful?
A: Consider WSGI. You have to pass 'environ' around *everywhere*. If you had
'environ' as a global, then different threads would really muck things up.
With Dynamic Scoping, you set 'environ' once in a dynamic scope, and all the
functions you call, and all the functions called by them, and so on and so
forth, have access to that unique 'environ'.

Q: What else is this good for?
A: Let's say you want to override configuration, such as what messages to log,
for all the functions in your code that are run as part of a single function.
With Dynamic Scoping, you can define the configuration at the global level,
and then allow individual functions to re-configure that configuration for all
functions called by them.

Q: How does this work?
A: If you want to create a variable in the dynamic scope, you have to use the
"with" syntax described above. This will create a new frame that will be
popped off once you exit that "with" block. 

Inside the "with" block, you frame is at the top until some other function
overrides it with their own "with" block. Whatever frames are already present
are still around, they're just below the new frame.

For variable access, the global object 'dynamic' looks at the top of the
stack. If it can't find the variable, the frame looks at the previous frame,
and so on.

Q: Are there alternative implementations?
A: Yes, possibly. I've tried, unsuccessfully, to get this to work with
sys.settrace().

Q: Why can't I assign to the dynamic scope without using a "with" block?
A: Because that's the only way I can tell when your scope starts and ends. If
it were possible to detect when your current frame expires, then I wouldn't
need the "with" block at all.

Q: Should Python adopt Dynamic Scoping into its core language?
A: HECK NO! People get along just fine without Dynamic Scoping, and seem to
have an intuitive understanding of it without realizing it when they encounter
a problem that Dynamic Scoping is perfect for. The workarounds are not all
that bad. What I'm doing here really isn't much different from what Pylons
does for its threadlocal globals.
"""

import threading

class Dynamic(object):

    def __init__(self, threadlocal):
        self._threadlocal = threadlocal
        self._threadlocal.dynamic_frame = None

    def __call__(self, **vars):
        return DynamicFrame(self._threadlocal, vars)

    def __getattr__(self, name):
        if not self._threadlocal.dynamic_frame:
            raise NameError("name %r is not defined" % name)

        return getattr(self._threadlocal.dynamic_frame, name)

class DynamicFrame(object):

    def __init__(self, threadlocal, vars):
        self._threadlocal = threadlocal
        self._vars = vars

        self._parent = self._threadlocal.dynamic_frame
        self._threadlocal.dynamic_frame = self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._threadlocal.dynamic_frame = self._parent

    def __getattr__(self, name):
        try:
            return self._vars[name]
        except KeyError:
            if self._parent:
                return getattr(self._parent, name)
            else:
                raise NameError("name %r is not defined" % name)

    def __setattr__(self, name, value):
        if name in ('_parent', '_vars', '_threadlocal'):
            return object.__setattr__(self, name, value)

        self._vars[name] = value

    def __delattr__(self, name):
        try:
            del self._vars[name]
        except KeyError:
            raise NameError("name %r is not defined" % name)


dynamic = Dynamic(threading.local())
