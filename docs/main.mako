<%page args="link, show_source, show_desc"/>

<%
  import os
  submodules = module.submodules()

  def shortName(name):
    return name[name.rfind('.') + 1:]
%>

<%def name="show_submodule(m)">
  <%
  innerSubmodules = m.submodules()
  innerSubmodules = sorted(innerSubmodules, key=lambda x: x.name)
  %>
  <dir style="padding-left: 10px;">
    <dt><code class="name">${link(m,shortName(m.name))}</code></dt>
    <dd>${show_desc(m)}</dd>
    % if innerSubmodules:
      % for m in innerSubmodules:
        ${show_submodule(m)}
      % endfor
    % endif
  </dir>
</%def>

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title></title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">

    <link rel="icon" href="https://assets-global.website-files.com/5fe1e5ab342569725c29e137/6023ddbbc894d982d390185a_circular-32.png" sizes="32x32" type="image/png">

    <style>
      pre code {
        font-style: normal;
        font-family: "Droid Sans Mono","Inconsolata","Menlo","Consolas","Bitstream Vera Sans Mono","Courier",monospace;
        background: #292929;
        color: #fafafa;
        font-size: 18px;
        padding: 18px;
        border-radius: 8px
      }

      .modal-dialog {
        pointer-events: inherit;
      }

      #lunr-search {
        width: 100%;
        font-size: 1em;
        padding: 6px 9px 5px 9px;
        border: 1px solid silver;
      }

    </style>

</head>

<body>

  <div class="col-lg-8 mx-auto p-4 py-md-5">
        <%include file="github-corner.mako"/>

        <header class="pb-3 mb-5 col-md-4">
          <%include file="logo.mako"/>
        </header>

        <main>

            <div class="col-12 col-md-12 mb-5">
              <h1>Macrobond Data API for Python</h1>
              <p class="fs-5 col-md-12">
                  The Macrobond Data API for Python is used to access the world’s most extensive macroeconomic, aggregate financial and sector database provided by <a href="http://www.macrobond.com">Macrobond</a>.
                  Exposes a common API in Python for the <a href="https://help.macrobond.com/technical-information/the-macrobond-data-web-api-feed/">Macrobond Web</a> and <a href="https://help.macrobond.com/technical-information/the-macrobond-api-for-python/">Client data</a> APIs
              </p>
              <p class="fs-5 col-md-12">
                  You have to be a licensed user and have a Data+ or data feed user account in order to use the API.
              </p>
            </div>

            <div class="col-12 col-md-12 mb-5">
              <h2>Installing macrobond-data-api and Supported Versions</h2>
              <p class="fs-5">
                Supported versions of Python are currently 3.7 - 3.11.
              </p>
              <p class="fs-5">
                The package is available at <a href="https://pypi.org/project/macrobond-data-api/">PiPy</a> and can be installed using this command:
              </p>
              <pre style="display: inline;"><code>python -m pip install macrobond-data-api</code></pre>
            </div>

            <div class="col-12 col-md-12 mb-5">
              <h2>Using of system keyring</h2>
              <p class="fs-5">
                When using WebClient it is recommended to use the system keyring.
                This can be done easily by running the include script using this command:
              </p>
              <pre style="display: inline;"><code>python -c "from macrobond_data_api.util import *; save_credential_to_keyring()"</code></pre>
            </div>
            <div class="col-12 col-md-12 mb-5">
              <h3>Supported keyrings</h3>
              <ul>
                <li>macOS <a href="https://en.wikipedia.org/wiki/Keychain_%28software%29">Keychain</a></li>
                <li>Freedesktop <a href="http://standards.freedesktop.org/secret-service/">Secret Service</a> supports many DE including GNOME (requires <a href="https://pypi.python.org/pypi/secretstorage">secretstorage</a>)</li>
                <li>KDE4 &amp; KDE5 <a href="https://en.wikipedia.org/wiki/KWallet">KWallet</a> (requires <a href="https://pypi.python.org/pypi/dbus-python">dbus</a>)</li>
                <li><a href="https://docs.microsoft.com/en-us/windows/uwp/security/credential-locker">Windows Credential Locker</a></li>
              </ul>
            </div>
            
            <div class="row g-5">
                <div class="col-md-6">
                    <h2>Index</h2>
                    <dl>
                      ${show_submodule(next(filter(lambda x: x.name.endswith("common"), submodules)))}
                      <hr class="col-md-6">

                      ${show_submodule(next(filter(lambda x: x.name.endswith("web"), submodules)))}
                      <hr class="col-md-6">
                      
                      ${show_submodule(next(filter(lambda x: x.name.endswith("com"), submodules)))}
                      <hr class="col-md-6">
                      
                      ${show_submodule(next(filter(lambda x: x.name.endswith("util"), submodules)))}
                      <hr class="col-md-6">
                    </dl>
                </div>
                  
                <div class="col-md-6">

                  <div class="col-md-12">
                      <h2>Examples</h2>
                      <p>You can find examples how to use the API <a href="https://github.com/macrobond/macrobond-api-examples">here</a>.</p>
                  </div>
      
                  <div class="col-md-12">
                      <h2>Getting support</h2>
                      <a href="https://help.macrobond.com/support/">Support options</a>
                  </div>
      
                  <div class="col-md-12">
                      <h2>Contributing</h2>
                      <p>...</p>
                  </div>
                
                </div>
            </div>
        </main>
    </div>

    % if http_server and module:  ## Auto-reload on file change in dev mode
        <script>
          var html = "";
          setInterval(() =>
              fetch(window.location.href)
                .then(response=> response.text())
                .then(newHtml => {
                  if(html == "")
                    html = newHtml;
                  if(html != newHtml)
                    window.location.reload();
                }), 1000);
        </script>
    % endif

</body>

</html>