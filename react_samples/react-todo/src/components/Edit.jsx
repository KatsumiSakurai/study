
const Edit = (props) => (
    <form className="siimple-form" onSubmit={props.handleSave}>
      <div className="siimple-form-field">
        <label className="siimple-label siimple--color-white">Your todo:</label>
        <input name="title" type="text" className="siimple-input" defaultValue={props.todo}/>　
        <label className="siimple-label siimple--color-white">Limit:</label>
        <input name="date" type="date" className="siimple-input" defaultValue={props.date}/>　
        <input type="submit" value="Save" className="siimple-btn siimple-btn--teal"/>
      </div>
    </form>
  );
  
  export default Edit;