```
           _    __                  _   
 __      _| |_ / _|_ __   ___  _ __| |_ 
 \ \ /\ / / __| |_| '_ \ / _ \| '__| __|
  \ V  V /| |_|  _| |_) | (_) | |  | |_ 
   \_/\_/  \__|_| | .__/ \___/|_|   \__|
                  |_|                   
```
# wtfport

[![PyPI version](https://img.shields.io/pypi/v/wtfport-cli.svg)](https://pypi.org/project/wtfport-cli)
[![Release](https://img.shields.io/github/v/release/anilrajrimal1/wtfport)](https://github.com/anilrajrimal1/wtfport/releases)
[![License](https://img.shields.io/github/license/anilrajrimal1/wtfport)](LICENSE)

**Discover what's binding your TCP/UDP ports with ease.**

`wtfport` is a lightweight, command-line tool designed to identify processes occupying specific TCP or UDP ports on your system. Perfect for developers, system administrators, and network troubleshooters, it delivers clear, actionable insights in seconds.

## Features

- **Instant Port Lookup**: Identify which process is using a TCP/UDP port in real-time.
- **Detailed Output**: View process name, PID, and uptime for active ports.
- **Intuitive Feedback**: Get clear confirmation when a port is free.
- **Cross-Platform**: Supports Linux, macOS, and Windows.
- **Lightweight**: Minimal dependencies for fast installation and execution.

## Installation

### From PyPI
Install the latest stable release via pip:

```bash
pip install wtfport-cli
```

### From Debian Package
For Debian-based systems, use the `.deb` package:
Find it in release page of this github repository.
```bash
sudo dpkg -i wtfport_1.0.0-1_all.deb
```

### From Source
To install from source, clone the repository and run:

```bash
git clone https://github.com/anilrajrimal1/wtfport.git
cd wtfport
pip install .
```

## 🛠 Usage

Check a port by running:

```bash
wtfport 6969
```

### Example Output
- **Port in Use**:
  ```plaintext
  Port 6969 is in use by `node server.js` (PID 1234) for 5h 12m 4s.
  ```

- **Port Free**:
  ```plaintext
  WOW! Nothing on port 6969, it's free!
  ```

## Requirements

- **Python**: 3.9 or higher
- **Dependencies**:
  - `psutil` (installed automatically via PyPI)

To manually install dependencies:

```bash
pip install psutil
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/any-awesome-feature`
3. Commit your changes: `git commit -m 'Add awesome feature'`
4. Push to the branch: `git push origin feature/awesome-feature`
5. Open a Pull Request.

See our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## Support

For bugs, feature requests, or questions, please file an issue on our [GitHub Issues page](https://github.com/anilrajrimal1/wtfport/issues).

## Acknowledgments

- Crafted with ❤️ by the `wtfport` team.
- Powered by the [`psutil` library](https://github.com/giampaolo/psutil).
- Inspired by the need for fast, reliable port debugging.

---

*Find the port, free the port, own the port.*  
Happy debugging! 🐞
```
