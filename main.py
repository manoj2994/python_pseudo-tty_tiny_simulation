import os
import select
import sys
import pty
import termios
import tty



def main():
    master, slave = pty.openpty()
    print("Master PTY:", master)
    print("Slave PTY:", slave)
    pid = os.fork()
    if pid == 0:
        # print("\nChild Process:")
        # print("Process ID:", os.getpid())
        # print("Parent's process ID:", os.getppid())
        os.close(master)
        # 2. Become a session leader (detaches from any previous controlling terminal)
        os.setsid()

        # Note: Acquiring a *new* controlling terminal typically involves opening a
        # terminal device file (e.g., /dev/ttyX) with specific flags (O_RDWR | O_NOCTTY)
        # and possibly using an ioctl(TIOCSCTTY) call. pty.spawn handles this complex part.
        # For this simplified example to run a shell within the same context, 
        # we can rely on file descriptor inheritance/redirection if needed,
        # but the key is the final execve call.
        path = "/bin/sh"
        args = ["myshell"]
        env = os.environ.copy()
        os.dup2(slave, 0)  # stdin
        os.dup2(slave, 1)  # stdout
        os.dup2(slave, 2)  # stderr
        try:
            os.execve(path, args, env)
        except OSError as e:
            print(f"Execution failed: {e}", file=sys.stderr)
            os._exit(1) # exit immediately on failure
    else:        
        # print("\nParent Process:")
        # print("Process ID:", os.getpid())
        # print("Child's process ID:", pid)
        os.close(slave)
        # Save current terminal settings so we can restore them later
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())  # Raw mode for direct input

        print("Interactive shell started (type 'exit' or Ctrl-D to quit)\n")
        try:
            while True:
                # Wait for input from either stdin or the master
                r, _, _ = select.select([sys.stdin, master], [], [])
                #print(f"Select returned: {r}")
                if sys.stdin in r:
                    data = os.read(sys.stdin.fileno(), 1024)
                    if not data:
                        break  # EOF
                    os.write(master, data)

                if master in r:
                    output = os.read(master, 1024)
                    if not output:
                        break
                    os.write(sys.stdout.fileno(), output)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            print("\n[Shell exited]")

    

if __name__ == "__main__":
    main()