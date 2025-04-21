import React from "react";

export default function Page(props) {
  let { title, children } = props;
  return (
    <React.Fragment>
      <h1 className="text-3xl font-bold my-4 ml-1">{title}</h1>
      {children}
    </React.Fragment>
  );
}
