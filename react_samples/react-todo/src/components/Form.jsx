let today = new Date();
let today_str = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();

const Form = (props) => (
  <form className="siimple-form" onSubmit={props.handleAdd}>
    <div className="siimple-form-field">
      <label className="siimple-label siimple--color-white">Your todo:</label>
      <input name="title" type="text" className="siimple-input"/>　
      <label className="siimple-label siimple--color-white">Limit:</label>
      <input name="date" type="date" className="siimple-input" defaultValue={today_str}/>　
      <input type="submit" value="Add" className="siimple-btn siimple-btn--teal"/>
    </div>
  </form>
);

export default Form;