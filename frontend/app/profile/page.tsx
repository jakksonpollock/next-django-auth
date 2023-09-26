const Profile = async () => {
	const url = "http://localhost:3000/api/";
	const res = await fetch(url, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Authorization: "Bearer " + localStorage.getItem("token"),
		},
	});
	const user = await res.json();
	if (res.ok && user) {
		console.log(user);
		return user;
	}
	return <div>Profile Page</div>;
};

export default Profile;
