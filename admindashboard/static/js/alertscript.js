 ;(function(ns) { // ns - namesapce into which tagify function should be set (in our case it is window)
  "use strict";
  
 
  loadPolyfills();
  
  let container, tagifyInput, focusedTag;
  /// HTML element that will be used as tag
  const TAG_ELEMENT = "span";
  /// tag item's close button's content (may be HTML)
  const TAG_BUTTON_CONTENT = "x";
  
  const KEYCODE = {
    "BACKSPACE": ["Backspace", 8],
    "DELETE": ["Delete", 46]
  };
  
  const defaultOptions = {
    // * What user can type to complete tag. We're using KeyboardEvent.key & KeyboardEvent.keyCode codes.
    delimeters: ["Enter", ",", 13 /*Enter*/, 188 /*Comma in English*/, 222 /*comma in Hebrew*/, 44 /*comma in English/Hebrew in keypress event*/], 
    // * Delimeter for tag items value as string representation (is used in serialize function)
    inputDelimeter: ",",
    // * Class for tagify container (for styling)
    containerClass: "o-tagify",
    // * Class for tagify items (tags) (for styling)
    tagClass: "o-tagify__item",
    // * Class for tagify item (tag) when it's focused before being removed
    tagFocusClass: "is-focused", 
    // * Class for tagify tag close button (for styling)
    tagBtnClass: "o-tagify__btn",
    // * Placeholder text for tagify input
    tagPrompt: "add tags",
    // * Type for inner tagify input [by default will be taken from the original input]
    inputType: null,
    // * Array of attributes which should be copied from the original input
    copyAttributes: [],
    // * Whether tag should be added onblur
    addTagOnBlur: false
  };
  
  /// object which will be returned to the user for further usage
  const tagifyObj = {
    originalInput: null, // original input element,
    tagifyInput: null,
    serialize: serialize, // function which will serialize tagify tags into string value
    destroy: destroy, // function which will destroy current tagify container
  };
  
  
  /*======================
       Main Function
  ======================*/
  /*
   * Provides stylized input field that creates tags from inputted text.
   * @param {HTMLElement} inpElem - Original input element the tag feature should be applied on.
   * @param {Object} opts - Options for further control on the tagify plugin.
   *  @subparam {Array} delimeters - Delimeters that user can type to complete tag. Should be compatible with KeyboardEvent.key & KeyboardEvent.keyCode [default values are: Enter key and "," comma]
   *  @subparam {String} outputDelimeter - Delimeter which will be used on serialized value of the tags [default value is "," comma].
   *  @subparam {String} containerClass - Class for stylizing tagify container.
   *  @subparam {String} tagClass - Class for stylizing tag item.
   *  @subparam {String} tagFocusClass - Class for stylizing tag item when it's focused (before removal).
   *  @subparam {String} tagBtnClass - Class for stylizing tag item's button for deletion.
   *  @subparam {String} tagPrompt - Value to be included in tagify input as placeholder.
   *  @subparam {String} inputType - Type for tagify input [by default type is taking from originally provided input].
   *  @subparam {Array} copyAttributes - Array of attributes which should be copied from originally provided input (e.g. required, name, etc...) [default value is empty array, i.e. no attribute will be copied]
   *  @subparam {Boolean} addTagOnBlur - Determines whether tag should be created on blur (i.e. when tagify input is lose focus) [default value is FALSE].
   * @return {Object} tagifyObject - Object with originally provided input element,
   * new created input reference and utility functions (serialize, destroy)
  */
  function init(inpElem, opts) {   
    if(!inpElem || inpElem.tagName !== "INPUT") { throw new TypeError('Tagify must be set on INPUT element'); }
    /// Note: default options will be overridden
    opts = Object.assign(defaultOptions, opts);
    // if input type hasn't been defined explicitly via options we take it from received input element
    opts.inputType = opts.inputType || inpElem.type;
    
    createTagifyContainer(opts);
    
    addEventsToTagifyContainer(container, opts);
   
    /// copy, specified, attributes from the original input, if provided
    if(defaultOptions.copyAttributes && defaultOptions.copyAttributes.length > 0)
    copyOrgInputAttributes(inpElem);
    
    addTagifyContainerIntoDOM(container, inpElem);
    
    // save original input element
    tagifyObj.originalInput = inpElem;
        
    tagifyObj.tagifyInput = tagifyInput;
    
    /// hide original input
    inpElem.style.display = "none";  
    
    return tagifyObj; /// returns API object for further usage
  };
  
 /*
  * Same description as tagify method
  * @return {Promise} - Promise with tagifyObject - Object with originally provided input element,
  * new created input reference and utility functions (serialize, destroy)
  */
  function initAsync(inpElem, opts) {   
    if(!inpElem || inpElem.tagName !== "INPUT") { throw new TypeError('Tagify must be set on INPUT element'); }
    /// Note: default options will be overridden
    opts = Object.assign(defaultOptions, opts);
    // if input type hasn't been defined explicitly via options we take it from received input element
    opts.inputType = opts.inputType || inpElem.type;
    
    createTagifyContainer(opts);
    
    addEventsToTagifyContainer(container, opts);
   
    /// copy, specified, attributes from the original input, if provided
    if(defaultOptions.copyAttributes && defaultOptions.copyAttributes.length > 0)
    copyOrgInputAttributes(inpElem);
    
    addTagifyContainerIntoDOM(container, inpElem);
    
    // save original input element
    tagifyObj.originalInput = inpElem;
    
    tagifyObj.tagifyInput = tagifyInput;
    
    /// hide original input
    inpElem.style.display = "none";  
    
    return Promise.resolve(tagifyObj); /// returns API object for further usage
  };

  
   
  /*======================
        Event Listeners
    ======================*/
  /*
  * When close/delete button on tag item is clicked
  */
  function onCloseBtnClick(e) {
    const current = e.target;

    /// if it doesn't close button, do nothing
    if(!current.classList.contains(defaultOptions.tagBtnClass)) { return; }
    
    const buttonParent = current.parentElement;
    /// removes tag from the container
    container.removeChild(buttonParent);
  };
  
  /*
  * When one of the provided delimeters (for adding tag item) in inner tagify input element is clicked.
  */
  function onInnerInputKeyDown(e) {
    const pressedKey = e.key || e.keyCode;
    /// if pressed key is not the valid operation key (e.g. comma, enter, etc...) or inner input is empty, do nothing
    if(!isValidKey(defaultOptions.delimeters, pressedKey) || !tagifyInput.value.trim()) { return; }

      resetFocusedTag()
    
      insertTag();
    
    e.preventDefault(); /// prevents delimeter from staying in inner input as value
  };
   
  /*
  * When backpsace/delete button (for tag items deletion) is clicked (tagify input should be focused, otherwise event won't fire)
  */
  function onContainerKeyDown(e) {
    const current = e.target;

    /// if keyup didn't occur on inner input or inner input is not empty, do nothing
    if(current !== tagifyInput || tagifyInput.value.length > 0) { return; }
    
    const pressedKey = e.key || e.keyCode;
    const isItBackspace = isValidKey(KEYCODE.BACKSPACE, pressedKey);
    const isItDelete = isValidKey(KEYCODE.DELETE, pressedKey);
    if(!isItBackspace && !isItDelete) { return; }
    
    const tagifyLastTag = getLastTag();
    /// if there are no tags
    if(!tagifyLastTag)  { return; }
    
    
    if(isItBackspace && !focusedTag) { /*if backsapse was clicked and there is no focused tag item*/
      focusedTag = tagifyLastTag;
      focusedTag.classList.add(defaultOptions.tagFocusClass);
      return;
    } else if(isItDelete || focusedTag) { /*if delete key was clicked or there is tag item that's already been focused (backspace was clicked)*/
      container.removeChild(tagifyLastTag);
      focusedTag = null;
    };
    
  };
  
  

  /*
  * When inner input lose its focus (only applicable when addTagOnBlur option is TRUE)
  */
  function onInnerInputBlur(e) {
      /// if inner input is empty, do nothing
      if(!tagifyInput.value.trim()) { return; }
    
      resetFocusedTag();
    
      insertTag();

      e.preventDefault(); /// prevents delimeter from staying in inner input as value    
  };
  
  
  
  /*======================
      Utility Functions
    ======================*/
  
  /*
  * Creates tagify container, and inner tagify input.
  * Applies appropriate options.
  * @param {Object} opts - Appropriate options for tagify container and inner input.
  */
  function createTagifyContainer(opts) {
    // Container
    container = document.createElement("div");
    container.classList.add(opts.containerClass);
    
    /// We might add ARIA attributes here \\\
    
    // Input child
    tagifyInput = document.createElement("input");
    tagifyInput.type = opts.inputType;
    tagifyInput.setAttribute("placeholder", opts.tagPrompt);
    
    container.appendChild(tagifyInput);
  };
  
  /*
  * Creates tag item and applies appropriate options to it.
  * @param {Object} opts - Appropriate options for tag item.
  * @param {HTMLElement} tagText -Tag item text value.
  * @return {HTMLElement} Created tag item element.
  */
  function createTag(opts, tagText) {
    // Tag
    const tag = document.createElement(TAG_ELEMENT);
    tag.classList.add(opts.tagClass);
    tag.textContent = tagText;
    
    // Tag Close Button
    const tagButton = document.createElement("button");
    tagButton.innerHTML = TAG_BUTTON_CONTENT;
    tagButton.classList.add(opts.tagBtnClass);
   
    tag.appendChild(tagButton);
    
    return tag;
  };
  
  /*
  * Adds event listeners into tagify container and inner tagify input.
  * @param {HTMLElement} tagifyContainer - HTML Element for tagify container.
  * @param {Object} opts - Appropriate options for creating events.
  */
  function addEventsToTagifyContainer(tagifyContainer, opts) {
    
    // Container Events \\
    
    /// event when close button on tag is clicked
    container.addEventListener("click", onCloseBtnClick);  
    
     /// event for removing tag from tagify container (e.g. when backspace/delete is clicked)
    container.addEventListener("keydown", onContainerKeyDown, true); 
      
    
    // Inner Input Events \\
    
   // event when delimeter input is added into inner input for creating tag
   tagifyInput.addEventListener("keydown", onInnerInputKeyDown); 
    
    // event when inner input is lost focus for creating tag
    if(opts.addTagOnBlur) /// only if addTagOnBlur is true
    tagifyInput.addEventListener("blur", onInnerInputBlur);  
  };
  
  /*
  * Adds tagify container into DOM.
  * @param {HTMLElement} tagifyContainer - HTML Element for tagify container.
  * @param {HTMLElement} orgInp - Originally provided input element.
  */
  function addTagifyContainerIntoDOM(tagifyContainer, orgInp) {
    
    const nextSibling = orgInp.nextElementSibling;
    const orgInpParent = orgInp.parentElement;
    
    if(nextSibling) { /*if original input has sibling element after him*/
      orgInpParent.insertBefore(tagifyContainer, nextSibling);
    } else { /*if original input is the last child of its parent*/
      orgInpParent.appendChild(tagifyContainer);
    }
    
  };
  
  /*
  * Determines whether provided key code is located into key codes array.
  * @param {Array} keyCodes - Array of predefined, valid key codes to check against.
  * @param {String/Number} keyCode - Provided key code to check.
  * @return {Boolean} TRUE if provided key code has been found, otherwise returns FALSE
  */
  function isValidKey(keyCodes, keyCode) {
    let result = false;
    result = keyCodes.some(function(v) {
       return v === keyCode;
    });
    return result;
  };
  
  /*
  * Gets last tag item from tagify container.
  * @return {HTMLElement} Last tagify item, otherwise returns NULL.
  */
  function getLastTag() {
    const containerChildren = getTags();
    return containerChildren.length > 0 ? containerChildren[containerChildren.length - 1] : null;
  };
  
  /*
  * Gets tagify items from tagify container.
  * @return {Array} found tagify items, otherwise returns an empty array.
  */
  function getTags() {
    return Array.from(container.querySelectorAll("." + defaultOptions.tagClass));
  };
  
  /*
  * Inserts tag item into tagify container, empty inner tagify input element.
  */
  function insertTag() {    
      const tag = createTag(defaultOptions, tagifyInput.value.trim());
    
      container.insertBefore(tag, tagifyInput);

      // empty tagify inner input value
      tagifyInput.value = null;  
  };
   
  /*
  * Resets focusedTag variable, removes focus class from the last tag item element.
  */
  function resetFocusedTag() {
      if(focusedTag) {
        focusedTag.classList.remove(defaultOptions.tagFocusClass);
        focusedTag = null;
      };
  };
  
      
  /*
  * Copies specified attributes from the original input element.
  * @param {HTMLElement} orgInp - Originally provided input element.
  */
  function copyOrgInputAttributes(orgInp) {

    defaultOptions.copyAttributes.forEach(function(attrName) {
       const attrVal = orgInp.getAttribute(attrName);

       if(attrVal != null) { /*attribute value can be empty string, but if attribute doesn't defined it returns NULL*/
         tagifyInput.setAttribute(attrName, attrVal)
       }
    });
    
  };
  
  
  /*====================================
   API Functions (For Returning Object)
  ======================================*/
  
  /*
  * Converts tag items' value into string representation, divided by output delimeter from options.
  * @return {String} string representation of the tag items, otherwise returns NULL.
  */
  function serialize() {
    const tags = getTags(); /// get all created tags;
    let result = null;
    
    if(tags.length > 0) { /*if there is one tag, at least.*/
      result = tags.map(function(tag) {
        /// Note we get first ChildNode of the tag, so order of the elements in tag should be persisted (e.g. first is the TextNode and then delete button)
        return tag.firstChild.textContent; 
      }).join(defaultOptions.outputDelimeter);
    };
    
    return result;
  };
  
  /*
  * Removes tagify container from DOM, deletes tagify Object's properties. 
  * @param {Function} callback - Function which will be called after all actions have been done.
  *  @subparam {HTMElement} originalInput - Callback function will receive single element which is originally provided input element.
  */
  function destroy(callback) {
      container.parentElement.removeChild(container);
       /// get link to original input to set it as the first element in a callback function
       const originalInput = this.orgInput;
    
      for(var key in this) {
         if(this.hasOwnProperty(key)) 
            {  delete this[key]; }         
      }
    
    /// user callback will be called with original input as the first element
    if(typeof callback === "function") { callback(originalInput); }  
  };
  
  
 
  /*--------------------
        Pollyfills
    --------------------*/
  /*
  * Loads polyfills if needed.
  */
  function loadPolyfills() {
      
      /*Object assign polyfill (https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)*/
     if (typeof Object.assign != 'function') {
        Object.assign = function(target, varArgs) { // .length of function is 2
          'use strict';
          if (target == null) { // TypeError if undefined or null
            throw new TypeError('Cannot convert undefined or null to object');
          }

          var to = Object(target);

          for (var index = 1; index < arguments.length; index++) {
            var nextSource = arguments[index];

            if (nextSource != null) { // Skip over if undefined or null
              for (var nextKey in nextSource) {
                // Avoid bugs when hasOwnProperty is shadowed
                if (Object.prototype.hasOwnProperty.call(nextSource, nextKey)) {
                  to[nextKey] = nextSource[nextKey];
                }
              }
            }
          }
          return to;
        };
      };

      /*Mini polyfill for Array.from without optional arguments (mapFunction [second argument], thisArg [third argument]) (https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Array/from)*/
      if(typeof Array.from !== "function") {
        Array.from = function(arrLikeObj) {
          return Array.prototype.slice.call(arrLikeObj, 0);
        }
      };
    
  };

  
  // adding tagify function into provided namespace
  ns.tagify = {
    init: init,
    initAsync: initAsync
  };
  
})(window);


/*

Inspired by JQuery plugin "Tagify" by Alicia Liu

https://github.com/alicial/jQuery.Tagify

*/

/*

LINKS:

https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key

https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode

https://codepen.io/lsirivong/pen/xrFGn

*/


/*---- T E S T ----*/
;(function() {
  "use strict";
   
  const inp = document.getElementById("tagInp");
  const serializeBtn = document.getElementById("ser-btn");
  const output = document.getElementById("output");
  const destroyBtn = document.getElementById("destroy-btn");
  
  // /*Using Tagify Plugin (Synchronously)*/
  // const tagifyObj = window.tagify.init(inp, { // tagify options
  //   addTagOnBlur: true, // tag will be added on blur
  //   copyAttributes: ["required"], /// attributes that will be copied from the original input element
  // });
  
  /*Using Tagify Plugin (Asynchronously)*/
  
  let tagifyObject;
  
  window.tagify.initAsync(inp, { // tagify options
    addTagOnBlur: true, // tag will be added on blur
    copyAttributes: ["required"], /// attributes that will be copied from the original input element
  }).then(function (tagifyObj) {
    const tagifyInp = tagifyObj.tagifyInput;
    tagifyInp.focus();
    tagifyObject = tagifyObj;
  });
   
  
  /*Adding EventListeners*/
  serializeBtn.addEventListener("click", serializeBtnOnClick);
  destroyBtn.addEventListener("click", destroyBtnOnClick);
   
  /*Event Listeners*/
  function serializeBtnOnClick(e) { /// display tag items in string representation
   const p = document.createElement("p");
    
    p.textContent = tagifyObject.serialize();
    
    output.appendChild(p);   

    $("#sendid").show();
    $("#ser-btn").hide();
    
  };
   
  function destroyBtnOnClick(e) {   // destroy tagify element and set tag items data into original input
    tagifyObject.originalInput.value = tagifyObject.serialize();
    
    tagifyObject.destroy(function(orgInp) {
      orgInp.removeAttribute("style");
    });
     
  };
  
  
})();