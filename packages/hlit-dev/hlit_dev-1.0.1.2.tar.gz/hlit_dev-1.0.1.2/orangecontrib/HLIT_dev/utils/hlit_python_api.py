import subprocess
import urllib.parse
import sys



def call_start_workflow(ip_port: str, key_name: str) -> int:
    """
    Calls a REST API endpoint using curl to start a workflow identified by key_name on the server at ip_port.

    This function is cross-platform (macOS/Windows) and uses subprocess to invoke curl safely.
    It URL-encodes the workflow key, handles various system and network errors,
    and returns 0 if everything went well, or 1 if any error occurred.

    Parameters:
    - ip_port (str): The IP address and port of the target server (e.g. "127.0.0.1:8000")
    - key_name (str): The workflow name to start (e.g. "chatbot basique")

    Returns:
    - int: 0 if success (HTTP 200), 1 otherwise (any failure or non-200 response)
    """

    try:
        # Validate input IP:port format
        if not ip_port or ':' not in ip_port:
            print(f"Error: Invalid IP:port format: {ip_port}", file=sys.stderr)
            return 1

        # URL-encode the workflow key
        encoded_key = urllib.parse.quote(key_name, safe='')

        # Construct the full URL
        url = f"http://{ip_port}/start-workflow/{encoded_key}"

        # Prepare the curl command with safe options
        curl_cmd = [
            "curl", "-X", "GET",
            url,
            "-H", "accept: application/json",
            "--fail",  # return non-zero if HTTP code >= 400
            "--silent",  # suppress output
            "--show-error",  # still show errors if any
            "--write-out", "%{http_code}",  # write only the HTTP status code
            "--output", "-"  # output response body to stdout
        ]

        # Run the curl command and capture output
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # Check curl execution status
        if result.returncode != 0:
            print(f"Error: curl execution failed: {result.stderr.strip()}", file=sys.stderr)
            return 1

        # Extract HTTP status code from the last 3 characters of output
        http_code = result.stdout[-3:]
        if http_code != "200":
            print(f"Error: Unexpected HTTP response code: {http_code}", file=sys.stderr)
            return 1

        print("Request succeeded with HTTP 200")
        return 0

    except FileNotFoundError:
        # Curl is not installed
        print("Error: curl is not installed on this system.", file=sys.stderr)
    except Exception as e:
        # Any other unexpected error
        print(f"Error: Unexpected exception: {str(e)}", file=sys.stderr)

    return 1




def call_kill_process(ip_port: str, key_name: str) -> int:
    """
    Calls a REST API endpoint using curl to kill a running process identified by key_name on the server at ip_port.

    This function is cross-platform (macOS/Windows) and uses subprocess to invoke curl safely.
    It URL-encodes the process key, handles various system and network errors,
    and returns 0 if everything went well, or 1 if any error occurred.

    Parameters:
    - ip_port (str): The IP address and port of the target server (e.g. "127.0.0.1:8000")
    - key_name (str): The name of the process to kill (e.g. "chatbot basique")

    Returns:
    - int: 0 if success (HTTP 200), 1 otherwise (any failure or non-200 response)
    """

    try:
        # Validate input IP:port format
        if not ip_port or ':' not in ip_port:
            print(f"Error: Invalid IP:port format: {ip_port}", file=sys.stderr)
            return 1

        # URL-encode the process name
        encoded_key = urllib.parse.quote(key_name, safe='')

        # Construct the full URL
        url = f"http://{ip_port}/kill-process/{encoded_key}"

        # Prepare the curl command with safe options
        curl_cmd = [
            "curl", "-X", "GET",
            url,
            "-H", "accept: application/json",
            "--fail",
            "--silent",
            "--show-error",
            "--write-out", "%{http_code}",
            "--output", "-"
        ]
        print(curl_cmd)
        # Run the curl command and capture output
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # Check curl execution status
        if result.returncode != 0:
            print(f"Error: curl execution failed: {result.stderr.strip()}", file=sys.stderr)
            return 1

        # Extract HTTP status code from the last 3 characters of output
        http_code = result.stdout[-3:]
        if http_code != "200":
            print(f"Error: Unexpected HTTP response code: {http_code}", file=sys.stderr)
            return 1

        print("Kill request succeeded with HTTP 200")
        return 0

    except FileNotFoundError:
        print("Error: curl is not installed on this system.", file=sys.stderr)
    except Exception as e:
        print(f"Error: Unexpected exception: {str(e)}", file=sys.stderr)

    return 1


def call_output_workflow(ip_port: str, key_name: str) -> int:
    """
    Calls a REST API endpoint using curl to retrieve the output of a workflow identified by key_name
    on the server at ip_port.

    This function is cross-platform (macOS/Windows) and uses subprocess to invoke curl safely.
    It URL-encodes the workflow key, handles various system and network errors,
    and returns 0 if everything went well, or 1 if any error occurred.

    Parameters:
    - ip_port (str): The IP address and port of the target server (e.g. "127.0.0.1:8000")
    - key_name (str): The workflow name to retrieve output for (e.g. "chatbot basique")

    Returns:
    - int: 0 if success (HTTP 200), 1 otherwise (any failure or non-200 response)
    """

    try:
        # Validate input IP:port format
        if not ip_port or ':' not in ip_port:
            print(f"Error: Invalid IP:port format: {ip_port}", file=sys.stderr)
            return 1

        # URL-encode the workflow key
        encoded_key = urllib.parse.quote(key_name, safe='')

        # Construct the full URL
        url = f"http://{ip_port}/output-workflow/{encoded_key}"

        # Prepare the curl command with safe options
        curl_cmd = [
            "curl", "-X", "GET",
            url,
            "-H", "accept: application/json",
            "--fail",
            "--silent",
            "--show-error",
            "--write-out", "%{http_code}",
            "--output", "-"
        ]

        # Run the curl command and capture output
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # Check curl execution status
        if result.returncode != 0:
            print(f"Error: curl execution failed: {result.stderr.strip()}", file=sys.stderr)
            return 1

        # Extract HTTP status code from the last 3 characters of output
        http_code = result.stdout[-3:]
        if http_code != "200":
            print(f"Error: Unexpected HTTP response code: {http_code}", file=sys.stderr)
            return 1

        print("Output request succeeded with HTTP 200")
        return 0

    except FileNotFoundError:
        print("Error: curl is not installed on this system.", file=sys.stderr)
    except Exception as e:
        print(f"Error: Unexpected exception: {str(e)}", file=sys.stderr)

    return 1