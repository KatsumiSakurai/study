import React, { Component } from 'react';
import Form from './Form';
import List from  './List';
import Edit from  './Edit';

export default class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      todo: [],
      showEdit: false,
      editIndex: 0,
    };
    this.file = null;
    this.handleAdd = this.handleAdd.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.handleSaveData = this.handleSaveData.bind(this);
    this.handleLoadData = this.handleLoadData.bind(this);
    this.handleSetFile = this.handleSetFile.bind(this);
  }

  // データ保存
  handleAdd(e){
    e.preventDefault();
    // フォームから受け取ったデータをオブジェクトに挿入して、stateのtodo配列に追加
    this.state.todo.push({title: e.target.title.value, date: e.target.date.value});
    // setStateを使ってstateを上書き
    this.setState({todo: this.state.todo});
    // inputのvalueを空に
    e.target.title.value = '';
  }

  // データ削除
  handleRemove(i){
    // todo配列からi番目から1つ目のデータを除外
    this.state.todo.splice(i,1);
    // setStateでtodo配列を上書き
    this.setState({todo: this.state.todo});
  }

  handleEdit(i) {
    // console.log(this.state.todo[i]['title']);
    this.setState({showEdit: true});
    this.setState({editIndex: i});

  }

  handleSave(e) {
    e.preventDefault();
    console.log(e.target.title.value);
    var todos = this.state.todo;
    // フォームから受け取ったデータをオブジェクトに挿入して、stateのtodo配列に追加
    todos[this.state.editIndex] = {title: e.target.title.value, date: e.target.date.value};
    // setStateを使ってstateを上書き
    this.setState({todo: todos});
    // inputのvalueを空に
    e.target.title.value = '';
    this.setState({showEdit: false});

  }

  handleSaveData() {
    const json = JSON.stringify(this.state.todo);
    const blob = new Blob([json], { type: 'text/json'});
    const jsonURL = URL.createObjectURL(blob);
    const link = document.createElement('a');
    document.body.appendChild(link);
    link.href = jsonURL;
    const now = new Date();
    const fname = 'todo_' + now.getFullYear() + (now.getMonth() + 1) + now.getDate() + "_" + now.getHours() + now.getMinutes() + now.getSeconds();
    link.setAttribute('download', fname);
    link.click();
    document.body.removeChild(link);
  }

  handleLoadData() {
    console.log(this.file);
    const reader = new FileReader();
    reader.onerror = () => this.reject(reader.error);
    reader.onload = () => this.resolve(reader.result || '');
    reader.readAsText(this.file);
  }

  reject(e) {
    console.log(e);
  }

  resolve(data) {
    const todos = JSON.parse(data);
    this.setState({todo: todos})
  }

  handleSetFile(e) {
    console.log(e.target.value);
    this.file = e.target.files[0];
  }

  render() {
    return (
      <div className="siimple-box siimple--bg-dark">
        <button onClick={this.handleSaveData}>保存</button>
        <button onClick={this.handleLoadData}>読込</button>
        <input type="file" name="jsonFile" className="file" accept="text/json" onChange={this.handleSetFile} />
        <h1 className="siimple-box-title siimple--color-white">React Todo App</h1>
        <Form handleAdd={this.handleAdd}/>
        <div className="siimple-rule"></div>
        <List todos={this.state.todo} handleRemove={this.handleRemove} handleEdit={this.handleEdit} />
        { this.state.showEdit
          ? <Edit
            handleSave={this.handleSave}
            todo={this.state.todo[this.state.editIndex]['title']}
            date={this.state.todo[this.state.editIndex]['date']}
            />
          : null }
      </div>
    );
 }
}
