# Changes in Python `asyncio`

## Python 3.9

<div style="color: #777">
Due to significant security concerns, the reuse_address parameter of asyncio.loop.create_datagram_endpoint() is no longer supported. This is because of the behavior of the socket option SO_REUSEADDR in UDP. For more details, see the documentation for loop.create_datagram_endpoint(). (Contributed by Kyle Stanley, Antoine Pitrou, and Yury Selivanov in bpo-37228.)

Added a new coroutine shutdown_default_executor() that schedules a shutdown for the default executor that waits on the ThreadPoolExecutor to finish closing. Also, asyncio.run() has been updated to use the new coroutine. (Contributed by Kyle Stanley in bpo-34037.)

Added asyncio.PidfdChildWatcher, a Linux-specific child watcher implementation that polls process file descriptors. (bpo-38692)

</div>

Added a new coroutine **asyncio.to_thread()**. It is mainly used for running IO-bound functions in a separate thread to avoid blocking the event loop, and essentially works as a high-level version of run_in_executor() that can directly take keyword arguments. (Contributed by Kyle Stanley and Yury Selivanov in bpo-32309.)

<div style="color: #777">
When cancelling the task due to a timeout, asyncio.wait_for() will now wait until the cancellation is complete also in the case when timeout is <= 0, like it does with positive timeouts. (Contributed by Elvis Pranskevichus in bpo-32751.)

asyncio now raises TypeError when calling incompatible methods with an ssl.SSLSocket socket. (Contributed by Ido Michael in bpo-37404.)

</div>

## Python 3.10

<div style="color: #777">
Add missing connect_accepted_socket() method. (Contributed by Alex Grönholm in bpo-41332.)
</div>

## Python 3.11

Added the **TaskGroup** class, an asynchronous context manager holding a group of tasks that will wait for all of them upon exit. For new code this is recommended over using create_task() and gather() directly. (Contributed by Yury Selivanov and others in gh-90908.)

Added **timeout()**, an asynchronous context manager for setting a timeout on asynchronous operations. For new code this is recommended over using wait_for() directly. (Contributed by Andrew Svetlov in gh-90927.)

<div style="color: #777">
Added the Runner class, which exposes the machinery used by run(). (Contributed by Andrew Svetlov in gh-91218.)
</div>

Added the **Barrier class** to the synchronization primitives in the asyncio library, and the related BrokenBarrierError exception. (Contributed by Yves Duprat and Andrew Svetlov in gh-87518.)

<div style="color: #777">
Added keyword argument all_errors to asyncio.loop.create_connection() so that multiple connection errors can be raised as an ExceptionGroup.

Added the asyncio.StreamWriter.start_tls() method for upgrading existing stream-based connections to TLS. (Contributed by Ian Good in bpo-34975.)

Added raw datagram socket functions to the event loop: sock_sendto(), sock_recvfrom() and sock_recvfrom_into(). These have implementations in SelectorEventLoop and ProactorEventLoop. (Contributed by Alex Grönholm in bpo-46805.)

Added cancelling() and uncancel() methods to Task. These are primarily intended for internal use, notably by TaskGroup.

</div>

## Python 3.12

<div style="color: #777">
The performance of writing to sockets in asyncio has been significantly improved. asyncio now avoids unnecessary copying when writing to sockets and uses sendmsg() if the platform supports it. (Contributed by Kumar Aditya in gh-91166.)
</div>

Add **asyncio.eager_task_factory()** and asyncio.create_eager_task_factory() functions to allow opting an event loop in to eager task execution, making some use-cases 2x to 5x faster. (Contributed by Jacob Bower & Itamar Oren in gh-102853, gh-104140, and gh-104138)

<div style="color: #777">
On Linux, asyncio uses asyncio.PidfdChildWatcher by default if os.pidfd_open() is available and functional instead of asyncio.ThreadedChildWatcher. (Contributed by Kumar Aditya in gh-98024.)

The event loop now uses the best available child watcher for each platform (asyncio.PidfdChildWatcher if supported and asyncio.ThreadedChildWatcher otherwise), so manually configuring a child watcher is not recommended. (Contributed by Kumar Aditya in gh-94597.)

Add loop_factory parameter to asyncio.run() to allow specifying a custom event loop factory. (Contributed by Kumar Aditya in gh-99388.)

Add C implementation of asyncio.current_task() for 4x-6x speedup. (Contributed by Itamar Oren and Pranav Thulasiram Bhat in gh-100344.)

asyncio.iscoroutine() now returns False for generators as asyncio does not support legacy generator-based coroutines. (Contributed by Kumar Aditya in gh-102748.)

asyncio.wait() and asyncio.as_completed() now accepts generators yielding tasks. (Contributed by Kumar Aditya in gh-78530.)

</div>

## Python 3.13

<div style="color: #777">
asyncio.as_completed() now returns an object that is both an asynchronous iterator and a plain iterator of awaitables. The awaitables yielded by asynchronous iteration include original task or future objects that were passed in, making it easier to associate results with the tasks being completed. (Contributed by Justin Arthur in gh-77714.)

asyncio.loop.create_unix_server() will now automatically remove the Unix socket when the server is closed. (Contributed by Pierre Ossman in gh-111246.)

DatagramTransport.sendto() will now send zero-length datagrams if called with an empty bytes object. The transport flow control also now accounts for the datagram header when calculating the buffer size. (Contributed by Jamie Phan in gh-115199.)

Add Queue.shutdown and QueueShutDown to manage queue termination. (Contributed by Laurie Opperman and Yves Duprat in gh-104228.)

Add the Server.close_clients() and Server.abort_clients() methods, which more forcefully close an asyncio server. (Contributed by Pierre Ossman in gh-113538.)

Accept a tuple of separators in StreamReader.readuntil(), stopping when any one of them is encountered. (Contributed by Bruce Merry in gh-81322.)

Improve the behavior of TaskGroup when an external cancellation collides with an internal cancellation. For example, when two task groups are nested and both experience an exception in a child task simultaneously, it was possible that the outer task group would hang, because its internal cancellation was swallowed by the inner task group.

In the case where a task group is cancelled externally and also must raise an ExceptionGroup, it will now call the parent task’s cancel() method. This ensures that a CancelledError will be raised at the next await, so the cancellation is not lost.

An added benefit of these changes is that task groups now preserve the cancellation count (cancelling()).

In order to handle some corner cases, uncancel() may now reset the undocumented \_must_cancel flag when the cancellation count reaches zero.

(Inspired by an issue reported by Arthur Tacca in gh-116720.)

When TaskGroup.create_task() is called on an inactive TaskGroup, the given coroutine will be closed (which prevents a RuntimeWarning about the given coroutine being never awaited). (Contributed by Arthur Tacca and Jason Zhang in gh-115957.)

The function and methods named create_task have received a new **kwargs argument that is passed through to the task constructor. This change was accidentally added in 3.13.3, and broke the API contract for custom task factories. Several third-party task factories implemented workarounds for this. In 3.13.4 and later releases the old factory contract is honored once again (until 3.14). To keep the workarounds working, the extra **kwargs argument still allows passing additional keyword arguments to Task and to custom task factories.

This affects the following function and methods: asyncio.create_task(), asyncio.loop.create_task(), asyncio.TaskGroup.create_task(). (Contributed by Thomas Grainger in gh-128307.)

</div>

## Future

**asyncio.eager_task_factory() might become the default task factory**, so make sure your code works nicely with it.
