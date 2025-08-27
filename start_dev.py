#!/usr/bin/env python3
"""Full-stack development server with auto-reload and port conflict handling."""
import subprocess
import sys
import time
import socket
import os
import signal
from pathlib import Path

def find_free_port(start_port=8000):
    """Find next available port starting from start_port."""
    port = start_port
    while port < start_port + 100:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
    raise RuntimeError(f"No free ports found starting from {start_port}")

def kill_processes_on_ports(ports):
    """Kill any processes running on specified ports."""
    for port in ports:
        try:
            if sys.platform == "win32":
                subprocess.run(f"netstat -ano | findstr :{port}", shell=True, capture_output=True)
            else:
                result = subprocess.run(f"lsof -ti:{port}", shell=True, capture_output=True, text=True)
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                            print(f"Killed process {pid} on port {port}")
                        except:
                            pass
        except:
            pass

def start_backend(backend_port):
    """Start FastAPI backend with auto-reload."""
    print(f"🚀 Starting backend on port {backend_port}...")
    
    env = os.environ.copy()
    env['PYTHONPATH'] = str(Path.cwd())
    
    return subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", str(backend_port),
        "--reload",
        "--reload-dir", str(Path.cwd() / "src"),
        "--reload-dir", str(Path.cwd() / "web" / "backend")
    ], cwd=Path.cwd() / "web", env=env)

def start_frontend(frontend_port, backend_port):
    """Start React frontend with auto-reload."""
    print(f"🎨 Starting frontend on port {frontend_port}...")
    
    # Update API base URL in environment
    env = os.environ.copy()
    env['REACT_APP_API_BASE'] = f'http://localhost:{backend_port}'
    env['PORT'] = str(frontend_port)
    env['BROWSER'] = 'none'  # Don't auto-open browser
    
    return subprocess.Popen([
        "npm", "start"
    ], cwd=Path.cwd() / "web" / "frontend", env=env)

def main():
    """Start full-stack development environment."""
    print("🔧 PPT Report Generator - Development Server")
    print("=" * 50)
    
    # Check if Node.js is available
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is required but not found. Please install Node.js from https://nodejs.org/")
        return
    
    try:
        subprocess.run(["npm", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm is required but not found. Please install Node.js from https://nodejs.org/")
        return
    
    # Find free ports
    backend_port = find_free_port(8000)
    frontend_port = find_free_port(3000)
    
    # Kill any existing processes on these ports
    kill_processes_on_ports([backend_port, frontend_port])
    
    print(f"📡 Backend will run on: http://localhost:{backend_port}")
    print(f"🌐 Frontend will run on: http://localhost:{frontend_port}")
    print("=" * 50)
    
    # Check dependencies
    web_dir = Path.cwd() / "web"
    frontend_dir = web_dir / "frontend"
    
    # Always check if react-scripts is available
    try:
        result = subprocess.run(["npm", "list", "react-scripts"], 
                              cwd=frontend_dir, capture_output=True, text=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, "npm list")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            print("✅ Frontend dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js and npm")
            return
    
    try:
        # Start backend
        backend_process = start_backend(backend_port)
        time.sleep(2)  # Give backend time to start
        
        # Start frontend
        frontend_process = start_frontend(frontend_port, backend_port)
        time.sleep(3)  # Give frontend time to start
        
        print("\n✅ Development servers started!")
        print(f"🔗 Open: http://localhost:{frontend_port}")
        print("\n📝 Features:")
        print("  • Auto-reload on code changes")
        print("  • Port conflict resolution")
        print("  • Full-stack hot reload")
        print("\n⏹️  Press Ctrl+C to stop all servers")
        
        # Wait for processes
        while True:
            if backend_process.poll() is not None:
                print("❌ Backend process died")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process died")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        try:
            backend_process.terminate()
            frontend_process.terminate()
            time.sleep(2)
            backend_process.kill()
            frontend_process.kill()
        except:
            pass
        print("✅ All servers stopped")

if __name__ == "__main__":
    main()