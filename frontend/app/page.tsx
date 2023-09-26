import {
	LoginButton,
	LogoutButton,
	ProfileButton,
	RegisterButton,
} from "@/components/button";

export default function Home() {
	return (
		<div className="flex justify-center items-center h-[70vh]">
			<LoginButton />
			<RegisterButton />
			<LogoutButton />
			<ProfileButton />
		</div>
	);
}
