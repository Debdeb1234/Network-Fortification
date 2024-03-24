import requests
import sys
import colorama
from colorama import Fore

colorama.init()


# Referrer-Policy check function
def check_referrer_policy_directive(referrer_policy_header, urlInput):
    directives = referrer_policy_header.split(', ')

    for directive in directives:
        directive = directive.strip()
        if directive in ['no-referrer', 'no-referrer-when-downgrade', 'origin', 'strict-origin', 'origin-when-cross-origin', 'strict-origin-when-cross-origin', 'same-origin', 'unsafe-url']:
            print("Navigation Website:", urlInput)
            print("Directive:", directive)

            # Add recommended referrer information based on the directive
            if directive == 'no-referrer':
                print("Referrer: no referrer sent")
            elif directive == 'no-referrer-when-downgrade':
                if urlInput.startswith('https://'):
                    print("Referrer:", urlInput)
                elif urlInput.startswith('http://'):
                    print("Referrer: no referrer sent")
            elif directive == 'origin':
                if urlInput.startswith('https://'):
                    print("Referrer: " + urlInput.split('//')[0] + "//" + urlInput.split('/')[2])
                else:
                    print("Referrer: no referrer sent")
            # Add handling for other directives here

        else:
            print("Invalid Referrer-Policy directive:", directive)

def check_csp_directives(csp_header):
    required_directives = ["script-src 'self'",]

    for directive in required_directives:
        if directive not in csp_header:
            print("Content Security Policy: Missing or incorrect directive:", directive)

def check_permissions_policy(permissions_policy_header):
    expected_policy = "geolocation=*, camera=*, microphone=*"
    
    if permissions_policy_header != expected_policy:
        print("Permissions Policy: Incorrect policy:", permissions_policy_header)
        print(Fore.RED + "[ERROR: Permissions policy should be '" + expected_policy + "']" + Fore.RESET)
    else:
        print("Permissions Policy: " + permissions_policy_header, end='\t\t')
        print(Fore.GREEN + '[OK]' + Fore.RESET)

def getURL():
    urlInput = input('Enter the URL: ')
    if urlInput.startswith('https://') or urlInput.startswith('http://'):
        url = urlInput
    else:
        url = 'http://' + urlInput

    try:
        response = requests.get(url)
    except requests.exceptions.SSLError:
        print(Fore.RED + "SSL CERTIFICATE NOT VERIFIED" + Fore.RESET)
        response = requests.get(url, verify=False)
    except requests.exceptions.Timeout:
        print(Fore.RED + "Connection has timed out." + Fore.RESET)
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        print(Fore.RED + "Too Many Redirects. Please try another URL" + Fore.RESET)
        sys.exit(1)
    except requests.HTTPError as exception:
        print(exception)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    print(response)

    checkHeaders(response, urlInput)

def checkHeaders(response, urlInput):
    headersPresent = response.headers
    secHeaders = {
        'Strict-Transport-Security': ['max-age=31536000', 'includeSubDomains'],
        'X-Frame-Options': ['deny'],
        'X-Content-Type-Options': ['nosniff'],
        'Content-Security-Policy': ['self'],
        'X-Permitted-Cross-Domain-Policies': ['none'],
        'Referrer-Policy': ['no-referrer', 'no-referrer-when-downgrade', 'origin', 'strict-origin', 'origin-when-cross-origin', 'strict-origin-when-cross-origin', 'same-origin', 'unsafe-url'],
        'Clear-Site-Data': ['cache', 'cookies', 'storage'],
        'Cross-Origin-Embedder-Policy': ['require-corp'],
        'Cross-Origin-Opener-Policy': ['same-origin'],
        'Cross-Origin-Resource-Policy': ['same-origin'],
        'Set-Cookie': ['httponly', 'secure'],
        'Cache-Control': ['no-cache', 'no-store'],
        'Pragma': ['no-cache'],
        'X-XSS-Protection': ['1', 'mode=block'],
        'Feature-Policy': [],
        'Permissions-Policy': ['geolocation=*, camera=*, microphone=*'],
    }

    missingHeader = []
    headersUsed = dict()
    removedHeaders = []

    for header in secHeaders.keys():
        if header not in headersPresent.keys():
            missingHeader.append(header)
        else:
            headersUsed[header] = headersPresent[header]


    printHeaders(headersUsed, missingHeader, secHeaders, urlInput)
    

def printHeaders(headersUsed, missingHeader, secHeaders, urlInput):
    print(' ')
    print('HEADERS USED ARE: ')

    for header, value in headersUsed.items():
        print(header + ' : ' + value, end='\t\t')
        if header == 'Content-Security-Policy' or header == 'Strict-Transport-Security' or header == 'Feature-Policy':
            print(' ')
            continue
        warn = 0
        for secValue in secHeaders[header]:
            if header == 'Set-Cookie' or header == 'Cache-Control':
                if headersUsed[header].lower().find(secValue) == -1:
                    print(Fore.YELLOW + '[WARNING: Must contain ' + secValue + ']' + Fore.RESET, end=' ')
                    warn = 1
                    continue
            else:
                if secValue.lower() not in [val.lower().strip() for val in value.split(';')]:
                    print(Fore.YELLOW + '[WARNING: Must contain ' + secValue + ']' + Fore.RESET, end=' ')
                    warn = 1
        if warn == 0:
            print(Fore.GREEN + '[OK]' + Fore.RESET, end=' ')
        print(' ')

    if len(missingHeader) > 0:
        print('\n' + Fore.RED + 'MISSING HEADERS ARE:' + Fore.RESET)
        for header in missingHeader:
            print(header, ' is missing', end='\t')
            if header == 'Content-Security-Policy' or header == 'Feature-Policy':
                print(' ')
                continue
            recommended = secHeaders[header]
            print(Fore.CYAN + '[Recommended:', end=' ')
            if len(recommended) == 1:
                for value in recommended:
                    print(value, end='')
            else:
                for value in recommended:
                    print(value, end=';')

            print(']' + Fore.RESET)

    # Extract and check the CSP header
    csp_header = headersUsed.get('Content-Security-Policy')
    if csp_header:
        check_csp_directives(csp_header)

    # Extract and check the Permissions-Policy header
    permissions_policy_header = headersUsed.get('Permissions-Policy')
    if permissions_policy_header:
        check_permissions_policy(permissions_policy_header)

# Call the getURL function to initiate header checks
getURL()
