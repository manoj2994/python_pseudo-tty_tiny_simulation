# python_pseudo-tty_tiny_simulation
This is a python program for simulating the pseudo-tty ,to recive input from keyboard and display the output

## 1. INPUT FLOW (Keyboard → Bash)
(1) You press a key
       │
       ▼
┌─────────────────────────────┐
│  Your real terminal window  │  (xterm, gnome-terminal, etc.)
└───────────────┬─────────────┘
                │ OS hands keystrokes to your process (Python)
                ▼
┌─────────────────────────────┐
│ Python Parent: sys.stdin    │  (reads from your real TTY)
└───────────────┬─────────────┘
         os.read│
                ▼
┌──────────────────────────────┐
│ Python writes to PTY Master  │
│   os.write(master_fd, key)   │
└─────────────┬────────────────┘
              │
              ▼
   ██████████████████████████████
   █  Linux Kernel TTY/PTY Driver█
   ██████████████████████████████
              │
       (a) Driver gets the byte
              │
       (b) Driver puts it into
           PTY-slave input buffer
              ▼
┌──────────────────────────────┐
│ PTY Slave (/dev/pts/N)       │
│ *Kernel buffers are here*    │
└─────────────┬────────────────┘
              │
    (c) Bash reads from this FD
              ▼
┌──────────────────────────────┐
│      Bash Shell (child)      │
│  reads input from slave pty  │
└──────────────────────────────┘

## OUTPUT FLOW (Bash → You)

┌──────────────────────────────┐
│    Bash shell writes output  │
│      to its stdout/stderr    │
└───────────────┬──────────────┘
                │ write()
                ▼
┌──────────────────────────────┐
│ PTY Slave (/dev/pts/N)       │  <--- write to slave
└───────────────┬──────────────┘
                │
   ███████████████████████████████
   █ Linux Kernel TTY/PTY Driver █
   ███████████████████████████████
                │
      (a) Driver receives data
                │
      (b) Driver copies it into
          PTY-master buffer
                ▼
┌──────────────────────────────┐
│ PTY Master (master_fd)       │  (held by Python)
└───────────────┬──────────────┘
          os.read│
                ▼
┌──────────────────────────────┐
│ Python Parent reads output   │
│     from master_fd           │
└───────────────┬──────────────┘
        os.write│ to sys.stdout
                ▼
┌──────────────────────────────┐
│ Your real terminal window    │
│ prints the bytes on screen   │
└──────────────────────────────┘


## Ref
i have found the below blog about the terminal very useful for better understanding

https://yatsushi.com/blog/python-pty-spawn-demystified/