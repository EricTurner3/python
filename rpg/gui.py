import atlastk as Atlas


body = """
        <div style="display: table; margin: 50px auto auto auto;">
        <fieldset>
            <input id="input" maxlength="20" placeholder="Enter a name here" type="text"
            data-xdh-onevent="Submit" value="World"/>
            <div style="display: flex; justify-content: space-around; margin: 5px auto auto auto;">
            <button data-xdh-onevent="Submit">Submit</button>
            </div>
        </fieldset>
        </div>
    """

class gui:
    def acConnect(self, this, dom, id):
        dom.setLayout("", body)
        dom.focus("input")


    # get the name
    def acSubmit(self, this, dom, id):
        return dom.getContent("input")
        

    def acClear(self, this, dom, id):
        if ( dom.confirm("Are you sure?") ):
            dom.setContent("input", "")
            dom.focus("input")

    callbacks = {
        "": acConnect,  # This key is the action label for a new connection.
        "Submit": acSubmit,
        "Clear": acClear,
    }
  
    Atlas.launch(callbacks)